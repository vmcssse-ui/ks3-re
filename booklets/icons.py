import os, urllib.request, cairosvg
NEED = ["sun","moon","feather","compass","map","flag","home","eye","music","film",
        "sunrise","wind","droplet","target","gift","smile","layers","trending-up",
        "user-check","anchor","coffee","umbrella","navigation","pen-tool","edit-3",
        "message-circle","thumbs-up","activity","aperture","box","camera","cloud",
        "crosshair","hexagon","mic","octagon","package","play-circle","radio",
        "scissors","send","triangle","tv","video","volume-2","watch","wifi","codepen"]
BASE="https://raw.githubusercontent.com/feathericons/feather/main/icons/%s.svg"
got=[]
for n in NEED:
    p="media/%s.png"%n
    if os.path.exists(p): got.append(n); continue
    try:
        svg=urllib.request.urlopen(BASE%n,timeout=15).read().decode()
    except Exception as e:
        print("miss",n,e); continue
    svg=svg.replace('stroke-width="2"','stroke-width="1.6"')
    cairosvg.svg2png(bytestring=svg.encode(),write_to=p,output_width=240,output_height=240)
    got.append(n)
print(len(got),"icons added")
