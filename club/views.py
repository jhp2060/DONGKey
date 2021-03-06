from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q

from .models import ApplyList
from .models import Club
from .models import ClubRule
from member.models import Member
from .forms import ClubForm
from .forms import ClubRuleForm
# Create your views here.


@login_required
def create_club(request):
    club_form = ClubForm(request.POST or None)
    if request.method == 'POST' and club_form.is_valid():
        club_form.save()
        member = Member.objects.create(
                club=club_form.instance,
                user=request.user,
                is_admin=True,
            )
        member.save()
        return redirect('core:main_page')
    ctx = {
        'club_form': club_form,
    }
    return render(request, 'club_entry.html', ctx)


@login_required
def read_admin_club(request, club):
    club = Club.objects.get(name=club)
    club_rule = ClubRule.objects.filter(club=club)
    apply_list = ApplyList.objects.filter(club__name=club)
    club_member = Member.objects.filter(club__name=club)
    ctx = {
        'club': club,
        'apply_list': apply_list,
        'member_list': club_member,
        'club_rule': club_rule,
    }
    return render(request, 'admin_club.html', ctx)


@login_required
def read_non_admin_club(request, club):
    club = Club.objects.get(name=club)
    ctx = {
        'club': club,
    }
    return render(request, 'as_member_club.html', ctx)


@login_required
def apply_club(request, club):
    club = Club.objects.get(name=club)
    if request.method == 'POST':
        apply_list = ApplyList.objects.create(
                club=club,
                user=request.user,
            )
        return redirect('core:main_page')

    else:
        return HttpResponse(status=404)


@login_required
def admit(request, pk, club):
    # admit 버튼 클릭 시 해당 계정을 ApplyList에서 지운다.
    # Member에 추가한다.
    # 권한은 0->1로
    apply_user = ApplyList.objects.get(user__pk=pk, club__name=club)
    if request.method == 'POST':
        Member.objects.create(
                club=apply_user.club,
                user=apply_user.user,
                is_admin=False,
            )
        apply_user.delete()
        return redirect(reverse('club:read_admin_club', kwargs={'club': club}))
    else:
        return HttpResponse(status=404)


@login_required
def create_club_rule(request, club):
    club_rule_form = ClubRuleForm(request.POST or None)
    if request.method == 'POST' and club_rule_form.is_valid():
        form = club_rule_form.save(commit=False)
        form.club = Club.objects.get(name=club)
        form.save()
        return redirect(reverse('club:read_admin_club', kwargs={'club': club}))
    return render(request, 'club_rule.html', {'club_rule_form': club_rule_form, })


@login_required
def update_club_rule(request, club, rule_pk):
    club_rule = ClubRule.objects.get(club__name=club, pk=rule_pk)
    form = ClubRuleForm(request.POST or None, instance=club_rule)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('club:read_admin_club', kwargs={'club': club}))
    return render(request, 'club_rule.html', {'club_rule_form': form, })


@login_required
def delete_club_rule(request, club, rule_pk):
    club_rule = ClubRule.objects.get(club__name=club, pk=rule_pk)
    club_rule.delete()
    return redirect('club:read_admin_club', kwargs={'club': club})
