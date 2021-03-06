import json
import requests

ACCESS_TOKEN = "" #put your access token between the quotes
ROOM_NAME = "" #give the room you will create a name
YOUR_MESSAGE = ""  #put the message that you will post to the room

#sets the header to be used for authentication and data format to be sent.
def setHeaders():         
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}     
	return (spark_header)

	
# creates a new room and returns the room id.
# Mission:  Add code to parse and return the room id
def createRoom(the_header,room_name):
	roomInfo = '{"title" :"' + room_name + '"}'
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.post(uri, data=roomInfo, headers=the_header)
	var = resp.json()
	print("createRoom JSON: ", var)
	#add code here to parse and return the room id.
    
	
# adds a new member to the room.  Member e-mail is test@test.com
def addMembers(the_header,roomId):
	member = '{"roomId":"' + roomId + '","personEmail": "test@test.com", "isModerator": false}'
	uri = 'https://api.ciscospark.com/v1/memberships'
	resp = requests.post(uri, data=member, headers=the_header)
	print("addMembers JSON: ", resp.json())

#posts a message to the room
def postMsg(the_header,roomId,message):
	message = '{"roomId":"' + roomId + '","text":"'+message+'"}'
	uri = 'https://api.ciscospark.com/v1/messages'
	resp = requests.post(uri, data=message, headers=the_header)
	print("postMsg JSON: ", resp.json())

#Mission write code to retrieve and display about the room
def getRoomInfo(the_header,roomId):
	print("In function getRoomInfo")	


if __name__ == '__main__':
    header=setHeaders()
	#passing the ROOM_NAME for the room to be created
    room_id=createRoom(header,ROOM_NAME) 
	#passing roomId to members function here to add member to the room.
    addMembers(header,room_id)   
	#passing roomId to message function here to Post Message to a room.
    postMsg(header,room_id,YOUR_MESSAGE) 
	
    
