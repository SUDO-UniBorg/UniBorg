"""
A Torrent Client Plugin Based On Aria2 for Userbot
cmds: Magnet link : .magnet magnetLink
	  Torrent file from local: .tor file_path
	  Show Downloads: .show
	  Remove All Downloads: .ariaRM
	  Resume All Downloads: .ariaResume
	  Pause All Downloads:  .ariaP
	  
By:- @Zero_cool7870	   
"""
import aria2p
from telethon import events
import asyncio
import os


cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"

aria2_is_running = os.system(cmd)

aria2 = aria2p.API(
		aria2p.Client(
			host="http://localhost",
			port=6800,
			secret=""
		)
	)


@borg.on(events.NewMessage(pattern=r"\.magnet", outgoing=True))
async def magnet_download(event):
	if event.fwd_from:
		return   
	var = event.text
	var = var[8:]
	
	magnet_uri = var
	magnet_uri = magnet_uri.replace("`","")
	print(magnet_uri)

	#Add Magnet URI Into Queue
	try:
		download = aria2.add_magnet(magnet_uri)
	except:
		await event.edit("`Error: Make Sure Magnet link is correct.`")	
		return

	await event.edit("`Downloading From Magnet Link: `\n\n"+magnet_uri+"\nType show to check status")
	await asyncio.sleep(5)
	await event.delete()		

@borg.on(events.NewMessage(pattern=r"\.tor", outgoing=True))
async def torrent_download(event):
	if event.fwd_from:
		return

	var = event.text[5:]
	
	torrent_file_path = var	
	torrent_file_path = torrent_file_path.replace("`","")
	print(torrent_file_path)

	#Add Torrent Into Queue
	try:
		download = aria2.add_torrent(torrent_file_path, uris=None, options=None, position=None)
	except:
		await event.edit("`Torrent File Not Found...`")
		return

	gid = download.gid
	complete = None
	while complete != True:
		file = aria2.get_download(gid)
		complete = file.is_complete
		try:
			msg = "Downloading File: "+str(file.name) +"\nSpeed: "+ str(file.download_speed_string())+"\n"+"Progress: "+str(file.progress_string())+"\nETA:  "+str(file.eta_string())+"\n\n"  	
			await event.edit(msg)
			await asyncio.sleep(10)
		except Exception as e:
			print(str(e))
			pass	

	await event.edit("File Downloaded Successfully:\n`"+download.name+"`")

@borg.on(events.NewMessage(pattern=r"\.url", outgoing=True))
async def magnet_download(event):
	if event.fwd_from:
		return
	var = event.text[5:]
	print(var)	
	uris = [var]

	#Add URL Into Queue 
	try:	
		download = aria2.add_uris(uris, options=None, position=None)
	except Exception as e:
		await event.edit("`Error:\n`"+str(e))
		return

	gid = download.gid
	complete = None
	while complete != True:
		file = aria2.get_download(gid)
		complete = file.is_complete
		try:
			msg = "Downloading File: "+str(file.name) +"\nSpeed: "+ str(file.download_speed_string())+"\n"+"Progress: "+str(file.progress_string())+"\nETA:  "+str(file.eta_string())+"\n\n"  	
			await event.edit(msg)
			await asyncio.sleep(10)
		except Exception as e:
			print(str(e))
			pass	
			
	await event.edit("File Downloaded Successfully...")


@borg.on(events.NewMessage(pattern=r"\.ariaRM", outgoing=True))
async def remove_all(event):
	if event.fwd_from:
		return
	try:
		removed = aria2.remove_all(force=True)	
		aria2.purge_all()
	except:
		pass
			
	if removed == False:  #If API returns False Try to Remove Through System Call.
		os.system("aria2p remove-all")

	await event.edit("`Removed All Downloads.`")  

@borg.on(events.NewMessage(pattern=r"\.ariaP", outgoing=True))
async def pause_all(event):
	if event.fwd_from:
		return
	paused = aria2.pause_all(force=True)	#Pause ALL Currently Running Downloads.

	await even.edit("Output: "+str(paused))

@borg.on(events.NewMessage(pattern=r"\.ariaResume", outgoing=True))
async def resume_all(event):
	if event.fwd_from:
		return

	resumed = aria2.resume_all()

	await event.edit("Output: "+str(resumed))	

@borg.on(events.NewMessage(pattern=r"\.show", outgoing=True))
async def show_all(event):
	if event.fwd_from:
		return
	output = "output.txt"
	#Show All Downloads
	downloads = aria2.get_downloads() 

	msg = ""

	for download in downloads:
		msg = msg+"File: "+str(download.name) +"\nSpeed: "+ str(download.download_speed_string())+"\n"+"Progress: "+str(download.progress_string())+"\nETA:  "+str(download.eta_string())+"\n\n"
	print(msg)
	if len(msg) <= 4096:
		await event.edit("`Current Downloads: `\n"+msg)
	else:
		await event.edit("`Output is huge. Sending as a file...`")
		with open(output,'w') as f:
			f.write(msg)
		await asyncio.sleep(2)	
		await event.delete()	
		await borg.send_file(
			event.chat_id,
			output,
			force_document=True,
            supports_streaming=False,
            allow_cache=False,
			reply_to=event.message.id,
			)				

