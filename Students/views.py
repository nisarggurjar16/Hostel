from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *

def Home(request):
    return render(request, 'index.html')


def PerferencesView(request):
    if request.user.is_anonymous:
        return redirect('home')
    user = request.user
    if user.is_staff:
        preferenced_students = User.objects.filter(is_staff=False)
    else:
        preferenced_students = User.objects.filter(is_staff=True)
    userPreference = Perferences.objects.filter(user = user).first()
    if request.method == 'POST':
        
        data = request.POST
        ch1 = User.objects.get(id = data['ch1'])
        ch2 = User.objects.get(id = data['ch2'])
        ch3 = User.objects.get(id = data['ch3'])
        ch4 = User.objects.get(id = data['ch4'])
        ch5 = User.objects.get(id = data['ch5'])
        if userPreference:
            userPreference.choice1 = ch1
            userPreference.choice2 = ch2
            userPreference.choice3 = ch3
            userPreference.choice4 = ch4
            userPreference.choice5 = ch5
            userPreference.save()
        else:
            Perferences.objects.create(user=user, choice1 = ch1, choice2 = ch2, choice3 = ch3, choice4 = ch4, choice5 = ch5)
    d = {"preferenced_students": preferenced_students, "userPreferences":userPreference}
    return render(request, 'preferences.html', d)


def Results(request):
    global err1
    err1 = False
    if not request.user.is_authenticated:
        return redirect('login')
    p = Perferences.objects.filter(user=request.user)
    if not p:
        return redirect('preferences')
    prefGrid = dict() 
    pref = Perferences.objects.all()
    toppers = [i.id for i in User.objects.filter(is_staff=True)]
    avgStudents = [
        i.id for i in User.objects.filter(is_staff=False)]
    toppers = toppers[1:]
    if len(toppers) > len(avgStudents):
        toppers = toppers[:len(avgStudents)]
    else:
        avgStudents = avgStudents[:len(toppers)]
    topPref = dict()
    avgPref = dict()
    for i in pref:
        if i.user.id == 1:
            pass
        else:
            prefGrid.update({i.user.id: [
                i.choice1.id, i.choice2.id, i.choice3.id, i.choice4.id, i.choice5.id]})
    for i in toppers:
        topPref.update({i: prefGrid[i]})
    for i in avgStudents:
        avgPref.update({i: prefGrid[i]})

    tentative_engagements = []

    free_toppers = []

    def init_free_topper():
        '''Initialize the arrays of women and men to represent 
            that they're all initially free and not engaged'''
        for top in topPref:
            free_toppers.append(top)

    def begin_matching(top):  # (man)
        '''Find the first free woman available to a man at
                any given time'''

        for avg in topPref[top]:

            # Boolean for whether woman is taken or not
            taken_match = [
                mate for mate in tentative_engagements if avg in mate]

            if (len(taken_match) == 0):
                # tentatively engage the man and woman
                tentative_engagements.append([top, avg])
                free_toppers.remove(top)

                break

            elif (len(taken_match) > 0):

                # Check ranking of the current dude and the ranking of the   'to-be' dude
                try:
                    current_mate = avgPref[avg].index(taken_match[0][0])
                    potential_mate = avgPref[avg].index(top)

                    if (current_mate < potential_mate):
                        pass
                    else:
                        # The new guy is engaged
                        free_toppers.remove(top)

                        # The old guy is now single
                        free_toppers.append(taken_match[0][0])

                        # Update the fiance of the woman (tentatively)
                        taken_match[0][0] = top
                        break
                except:
                    global err1
                    err1 = True
                    pass

    def stable_matching():
        '''Matching algorithm until stable match terminates'''
        while (len(free_toppers) > 0):
            for top in free_toppers:
                begin_matching(top)

    def get_free_students(RoomMates):
        users = list(User.objects.values_list('id', flat=True))
        engaged = list()
        free = list()
        for i in RoomMates:
            engaged.extend(i)
        for j in users:
            if j not in engaged:
                free.append(j)
        free = User.objects.filter(id__in = free)
        print(free)
        return free
        
    def main():
        init_free_topper()
        stable_matching()
        return tentative_engagements

    RoomMates = main()
    free = get_free_students(RoomMates)
    print(free)
    Roomies = list()
    for i in RoomMates:
        p1 = User.objects.get(id=i[0])
        p2 = User.objects.get(id=i[1])
        Roomies.append([p1.username, p2.username])
    return render(request, 'result.html', {"roomies":Roomies, 'free':free})
