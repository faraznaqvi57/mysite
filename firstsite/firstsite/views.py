from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
import json , requests



def home_page(request):
    global match
    global live_score_url
    match_url="https://cricapi.com/api/matches?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3"
    response=requests.get(match_url)
    data=json.loads(response.text)
    match=data['matches']
    list_of_live_score = []
    for i in match:
        i["team_1"] = i.pop("team-1")
        i["team_2"] = i.pop("team-2")

####################### Live score section#############################
        if i['matchStarted'] and (i['type'] == "ODI" or i['type'] == "Tests" or i['type'] == "Twenty20"):
            live_score_url='https://cricapi.com/api/cricketScore?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&unique_id='
            live_score_url_final=live_score_url+str(i['unique_id'])
            response=requests.get(live_score_url_final)
            live_score_data=json.loads(response.text)
            live_score_data["team_1"] = live_score_data.pop("team-1")
            live_score_data["team_2"] = live_score_data.pop("team-2")
            list_of_live_score.append(live_score_data)

    #################Calender section############################
    global calender_data
    calender_url="https://cricapi.com/api/matchCalendar?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3"
    response=requests.get(calender_url)
    data=json.loads(response.text)
    calender_data=data['data']

    ###########################previous match details###############################
    list_of_match_details_id=[]

    for match_detail in match:
        days=0
        x=0
        month=0
        y=0
        if (match_detail['type'] == "ODI" or match_detail['type'] == "Tests" or match_detail['type'] == "Twenty20"):
            date=match_detail['date']
            days=date[8]+date[9]
            months=date[5]+date[6]
            months=int(months)
            days=int(days)

            today_day=datetime.now()
            x=today_day.day
            y=today_day.month


            if months>=y:
                if days>=x:
                    list_of_match_details_id.append(match_detail['unique_id'])
    global list_of_matches
    list_of_matches=[]
    for id in list_of_match_details_id:
        url = "https://cricapi.com/api/fantasySummary?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&unique_id="+ str(id)
        response = requests.get(url)
        data = json.loads(response.text)
        count=0
        data['unique_id']=id
        for team in data['data']['team']:
            if count==0:
                data['team_1']=team['name']
                count=count+1
            else:
                data['team_2']=team['name']
        list_of_matches.append(data)
    global id_search
    id_search = 1

    context={
        "matches":match,
        "live_score":list_of_live_score,
        "id1":id_search,
        "previous_matches":list_of_matches
    }
    return render(request,"home1.html",context)

def match_calender(request):

    context={
        "calender_data":calender_data,
    }


    return render(request,'match_calender.html',context)
def batting_record(data,match_type):
    dict = {}
    SR = (data['data']['batting'][match_type]['SR'])
    Ave = (data['data']['batting'][match_type]['Ave'])
    Runs = (data['data']['batting'][match_type]['Runs'])
    Inns = (data['data']['batting'][match_type]['Inns'])
    fifty = (data['data']['batting'][match_type]['50'])
    hundered = (data['data']['batting'][match_type]['100'])
    if Inns == '' or Inns == '-':
        Inns = "0"
    if Runs == '' or Runs == '-':
        Runs = '0'
    if Inns != '0':
        Inn = float(int(Runs) / int(Inns))
    else:
        Inn = 0
    if SR == "" or SR == '-':
        SR = "0"
    strikeRate = float(SR)
    if Ave == "" or Ave == '-':
        Ave = '0'
    Avg = float(Ave)
    runs = int(Runs)
    if fifty == '' or fifty == '-':
        fifty = '0'
    if hundered == '' or hundered == '-':
        hundered = '0'
    fifties = int(fifty)
    hundereds = int(hundered)
    if strikeRate > 120:
        strikeRate += 10
    if Avg >= 50:
        Avg += 10
    if Avg > 32 and Avg < 50:
        Avg += 5
    if Inn > 30:
        Inn += 10

    strikeRate = (strikeRate / 200) * 100
    if fifties > 25:
        fifties = fifties / 8
    else:
        fifties = fifties / 10
    if hundereds > 25:
        hundereds = hundereds / 8
    else:
        hundereds = hundereds / 10
    total = (strikeRate + Avg + Inn + fifties + hundereds) / 5
    dict["name"] = data['name']
    dict['playingRole']=data['playingRole']
    dict["total"] = str(total)
    dict['pid']=data['pid']
    return dict
   # print(dict)
def bowling_record(data,match_type):
    dict={}
    Econ = (data['data']['bowling'][match_type]['Econ'])
    Ave = (data['data']['bowling'][match_type]['Ave'])
    Runs = (data['data']['bowling'][match_type]['Runs'])
    Inns = (data['data']['bowling'][match_type]['Inns'])
    Wkts = (data['data']['bowling'][match_type]['Wkts'])
    Balls = (data['data']['bowling'][match_type]['Balls'])
    if Econ=='' or Econ=='-':
        Econ='0'
    if Ave==''or Ave=='-':
        Ave='0'
    if Runs=='' or Runs=='-':
        Runs='0'
    if Inns==''or Inns=='-':
        Inns='0'
    if Wkts=='' or Wkts=='-':
        Wkts='0'
    if Balls==''or Balls=='-':
        Balls='0'
    avg=float(Ave)
    if avg<35:
        avg=avg+5
    econ=(float(Econ)/6)*100
    if econ<5:
        econ=econ+5
    inns=(int(Wkts)/int(Inns))*100
    if inns<200:
        inns=inns+10
    run=(int(Runs)/int(Balls))*100
    total=(avg+econ+inns+run)/4
    dict["name"] = data['name']
    dict['playingRole']=data['playingRole']
    dict["total"] = str(total)
    dict['pid'] = data['pid']
    return dict


def player_accuracy(data,match_type):
    if data['playingRole']=="Top-order batsman" or data['playingRole']=="Opening batsman" or data['playingRole']=="Middle-order batsman":
        player_record_demo=batting_record(data,match_type)
    elif data['playingRole']=="Bowler":
        player_record_demo=bowling_record(data,match_type)
    elif data['playingRole']=="Wicketkeeper batsman":
        player_record_demo=batting_record(data,match_type)
    elif data['playingRole']=="Allrounder" or data['playingRole']== "Bowling allrounder" or data['playingRole']== "Batting allrounder":
        player_record_demo1=batting_record(data,match_type)
        player_record_demo2=bowling_record(data,match_type)
        player_record_demo ={}
        player_record_demo['name']=player_record_demo1['name']
        player_record_demo['playingRole']=player_record_demo1['playingRole']
        player_record_demo['total']=(float(player_record_demo1['total'])+float(player_record_demo2['total']))/2
        player_record_demo['pid'] = player_record_demo1['pid']
    else:
        player_record_demo=batting_record(data,match_type)


    return player_record_demo



def detail_player_anylize(data,match_type):
    if data['data']['batting'][match_type]:
        player_accuracy_details=player_accuracy(data,match_type)
    else:
        firstclass='firstClass'
        player_accuracy_details=player_accuracy(data,firstclass)
    return player_accuracy_details

def anylize_player(squad,match_type):
    list_of_detail_player=[]
    for team in squad:
        for player_id in team['players']:
            player_url = "https://cricapi.com/api/playerStats?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&pid=" + str(player_id['pid'])
            response = requests.get(player_url)
            data_player = json.loads(response.text)
            list_of_detail_player.append(detail_player_anylize(data_player,match_type))
    #print(list_of_detail_player)
    return list_of_detail_player


def custom_team(request,id,match_type):
    url="https://cricapi.com/api/fantasySquad?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&unique_id="+str(id)
    response=requests.get(url)
    data=json.loads(response.text)
    squad=data["squad"]
    final_squad=anylize_player(squad,match_type)#id['match_type']

    context={
        "current_match":final_squad,
        "id1":id_search
    }
    return render(request,'custon_match.html',context)

def custom_match(request):
    list_of_custom_match=[]
    for custom_match in match:
        dict={}
        if custom_match['type'] == "ODI" or custom_match['type'] == "Tests" or custom_match['type'] == "Twenty20":
            #if custom_match['matchStarted'] is True:
                dict['team_1']=custom_match['team_1']
                dict['team_2'] = custom_match['team_2']
                dict["unique_id"]=custom_match["unique_id"]
                dict['type']=custom_match['type']
                dict['squad']=custom_match['squad']
                dict['dateTimeGMT']=custom_match['dateTimeGMT']
                list_of_custom_match.append(dict)

    context={
        "custom_match":list_of_custom_match,
        "id1":id_search
    }
    return render(request,"custom_match_details.html",context)



def match_details(request,id):
    url = "https://cricapi.com/api/fantasySummary?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&unique_id=" + str(id)
    response = requests.get(url)
    data = json.loads(response.text)
    count=0
    for team in data['data']['team']:
        if count == 0:
            data['team_1'] = team['name']
            count = count + 1
        else:
            data['team_2'] = team['name']

   # data[data['data']['batting']['score']['dismissal_info']]=data.pop(data['data']['batting']['score']['dismissal-info'])
    man_of_the_match= data['data']['man-of-the-match']

    context={
            "data_summary":data,
            "team_1":data['team_1'],
            "team_2": data['team_2'],
            "man_of_the_match":man_of_the_match,
            "id1":id_search
        }

    return render(request,"match_details.html",context)

def prediction(request,id):

    for match_details in match:
        if match_details['unique_id']==id:
            match_type=match_details['type']
            match_squad=match_details['squad']
            match_team_1 = match_details['team_1']
            match_team_2 = match_details['team_2']
            break
    url = "https://cricapi.com/api/fantasySquad?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&unique_id="+str(id)
    response = requests.get(url)
    data = json.loads(response.text)
    if match_squad is True:
        squad = data["squad"]
        final_squad = anylize_player(squad, match_type)
        count=0
        sum1=0
        sum2=0
        for player in final_squad:
            if count <15:
                sum1=sum1+float(player['total'])
                count+=1
            else:
                sum2=sum2+float(player['total'])
                count+=1
        team1_sum=(sum1/15)
        team2_sum=(sum2/15)

        context={
            'team1_name':match_team_1,
            'team2_name': match_team_2,
            "team1_sum":team1_sum,
            "team2_sum":team2_sum,
            "id1":id_search
        }
    else:
        context = {
            'team1_name': match_team_1,
            'team2_name': match_team_2,
            "squad_not_found":"squad not available",
            "id1":id_search
        }

    return render(request,"prediction.html",context)



def search(request,id):
    print(id)
    if id==1:
        query=request.GET.get("text","off")
        pid = []
        url = 'https://cricapi.com/api/playerFinder?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&name='+ query

        resp = requests.get(url)
        data = json.loads(resp.text)
        player = data['data']

        for i in player:
            key_list = list(i.keys())
            val_list = list(i.values())
            pid.append(val_list[key_list.index("pid")])

        list_data = []

        for unique_id in pid:
            url2 = "https://cricapi.com/api/playerStats?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&pid=" + str(unique_id)
            response = requests.get(url2)
            data_player = json.loads(response.text)

            list_data.append(data_player)
    else:
        url2 = "https://cricapi.com/api/playerStats?apikey=ZSTtSDmD3eU8nGyPeXNNJEaAU1F3&pid=" + str(id)
        response = requests.get(url2)
        data_player = json.loads(response.text)
        list_data=list(data_player)




    context={
        "player_data":list_data,
        "id1":id_search


     }

    return render(request,"search.html",context)



def aboutus(request):
    return render(request,'aboutus.html')