from redbot.core.utils.chat_formatting import pagify 
import re
from redbot.core import commands
import webbrowser
import random as rand
import discord
import sqlite3
import math
import numpy as np
import datetime
from redbot.core import bank, commands,checks
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

def charge(amount: int):
    async def pred(ctx):
        try:
            await bank.withdraw_credits(ctx.author, amount)
        except ValueError:
            return False
        else:
            return True

    return commands.check(pred)
def givec(amount: int):
    async def pred(ctx):
        try:
            await bank.deposit_credits(ctx.author, amount)
        except ValueError:
            return False
        else:
            return True
    return commands.check(pred)
class Pokemon():
        hp:int
        atk:int
        defense:int
        spatk:int
        spdef:int
        speed:int
        lv:int
        evs:[int,int,int,int,int,int]
        nature:str
        ability:str
class blaze(commands.Cog):
    """Blazibot -- A Pokemon Bot"""
    def __init__(self, bot):
        self.bot = bot
        self.count=0
    @commands.command(name="redeem",aliases=["r"])
    async def redeem(self, ctx,redeemable:str):
        author=ctx.author.id
        a=ctx.author
        conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute(f"select redeems from Profile where user_name='{str(author)}'")
        deemamt=c.fetchone()
        deemamt=str(deemamt).strip("(").strip(")").strip(",").strip("'")
        deemamt=int(deemamt)
        if redeemable.casefold().capitalize()=='Blaze-tokens' and deemamt>0:
            try:
                await bank.deposit_credits(a, 1000)
                await ctx.send("you have redeemed 1000 Blaze-tokens!")
                deems=int(deemamt)-1
                await ctx.send(str(deems))
                c.execute(f"update Profile set redeems={int(deems)} where user_name={str(author)}")
                conn.commit()
            except ValueError:
                await ctx.send('You could not redeem')
                return False
            else:
                return True
            await ctx.send("you have redeemed 1000 credits!")
            deems=int(deemamt)-1
            conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"update Profile set redeems={int(deems)} where user_name={str(author)}")
            conn.commit()

        else:
            conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"select number from poke where Name='{str(redeemable)}'")
            deemedpoke=c.fetchone()
            deemedpoke=str(deemedpoke).strip("(").strip(")").strip(",").strip("'")
            c.execute(f"select redeems from Profile where user_name='{str(author)}'")
            deemamt=c.fetchone()
            deemamt=str(deemamt).strip("(").strip(")").strip(",").strip("'")
            
            if 'No' in deemedpoke:
                await ctx.send("That pokemon doesn't exist!")
            elif deemamt<='0':
                await ctx.send(str(deemamt))
                await ctx.send("You dont have any redeems!")
                
            else:
                try:
                    conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')
                    c = conn.cursor()
                    randlevel=5
                    randhp=rand.randint(0,31)
                    randatk=rand.randint(0,31)
                    randdef=rand.randint(0,31)
                    randsp_atk=rand.randint(0,31)
                    randsp_def=rand.randint(0,31)
                    randsp=rand.randint(0,31)
                    c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                    numberofpokes=c.fetchall()
                    noofpokes=len(numberofpokes)
                    newnumberofpokes=noofpokes+1
                    itemdrop='None'
                    c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),int(deemedpoke),str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                    conn.commit()
                    deems=int(deemamt)-1 
                    await ctx.send(str(deems))
                    c.execute(f"update Profile set redeems={int(deems)} where user_name='{str(author)}'")
                    conn.commit()
                    c.close()
                except:
                    await ctx.send('You could not redeem a pokemon! :(')
                
    @commands.command(name="moves",aliases=["like-jagger"])
    async def moves(self, ctx):
        author=ctx.author.id
        conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute(f"select numbercaught from selected where owner={author}")
        selectedstuff=c.fetchone()
        numcaught=str(selectedstuff)
        numcaught=str(numcaught).strip(",").strip(")").strip("(")
        numcaught=numcaught[:-1]
        c.execute(f"select move1,move2,move3,move4 from ownedpokes where owner={author} and numbercaught={numcaught}")
        moves=c.fetchall()
        embed=discord.Embed(title="Moves")
        for m in moves:
            embed.add_field(name="-", value=m ,inline=True)
        await ctx.send(embed=embed)
        c.close()
    @commands.command(name="learn",aliases=['teach'])
    async def learn(self, ctx,movename:str,slotnumber:str):
        author=ctx.author.id
        conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute(f"select id from selected where owner={author}")
        pokeid=c.fetchone()
        pokeid=str(pokeid).strip(",").strip(")").strip("(")
        pokeid=pokeid[:-1]
        await ctx.send(pokeid)
        c.execute(f"select type from poke where number={pokeid}")
        typeofpoke=c.fetchone()
        typeofpoke=str(typeofpoke).strip(",").strip(")").strip("(")
        typeofpoke=typeofpoke[:-1]
        typeofpoke=typeofpoke[:-1]
        typeofpoke=typeofpoke[1:]
        
        await ctx.send(typeofpoke)
        mt=["-","-"]
        if 'Fire' in typeofpoke:
            mt.append('fire')
        if 'Steel' in typeofpoke:
            mt.append('steel')
        if 'Ghost' in typeofpoke:
            mt.append('ghost')
        if 'Bug' in typeofpoke:
            mt.append('bug')
        if 'Rock' in typeofpoke:
            mt.append('rock')
        if 'Ground' in typeofpoke:
            mt.append('ground')
        if 'Poison' in typeofpoke:
            mt.append('poison')
        if 'Flying' in typeofpoke:
            mt.append('flying')
        if 'Fighting' in typeofpoke:
            mt.append('fighting')
        if 'Grass' in typeofpoke:
            mt.append('grass')
        if 'Electric' in typeofpoke:
            mt.append('electric')
        if 'Water' in typeofpoke:
            mt.append('water')
        if 'Psychic' in typeofpoke:
            mt.append('psychic')
        if 'Ice' in typeofpoke:
            mt.append('ice')
        if 'Dragon' in typeofpoke:
            mt.append('dragon')
        if 'Dark' in typeofpoke:
            mt.append('dark')
        if 'Fairy' in typeofpoke:
            mt.append('fairy')
        if 'Normal' in typeofpoke:
            mt.append('normal')
        mt.append(" ")
        t1=mt[2]
        if(str(mt[3])==" "):
            t2="-"
        else:
            t2=str(mt[3])
        await ctx.send(t1+t2)
        numtype=["",""]
        fire=10
        steel=9
        ghost=8
        bug=7
        rock=6
        ground=5
        poison=4
        flying=3
        fighting=2
        water=11
        grass=12
        electric=13
        psychic=14
        ice=15
        dragon=16
        dark=17
        fairy=18
        normal=1
        if 'fire' in mt:
            numtype.append(fire)
        if 'steel' in mt:
            numtype.append(steel)
        if 'ghost' in mt:
            numtype.append(ghost)
        if 'bug' in mt:
            numtype.append(bug)
        if 'rock' in mt:
            numtype.append(rock)
        if 'ground' in mt:
            numtype.append(ground)
        if 'poison' in mt:
            numtype.append(poison)
        if 'flying' in mt:
            numtype.append(flying)
        if 'fighting' in mt:
            numtype.append(fighting)
        if 'grass' in mt:
            numtype.append(grass)
        if 'electric' in mt:
            numtype.append(electric)
        if 'water' in mt:
            numtype.append(water)
        if 'psychic' in mt:
            numtype.append(psychic)
        if 'ice' in mt:
            numtype.append(ice)
        if 'dragon' in mt:
            numtype.append(dragon)
        if 'dark' in mt:
            numtype.append(dark)
        if 'fairy' in mt:
            numtype.append(fairy)
        if 'normal' in typeofpoke:
            numtype.append(normal)
        numtype.append(" ")
        fire=10
        steel=9
        ghost=8
        bug=7
        rock=6
        ground=5
        poison=4
        flying=3
        fighting=2
        water=11
        grass=12
        electric=13
        psychic=14
        ice=15
        dragon=16
        dark=17
        fairy=18
        normal=1
        await ctx.send(numtype)
        possibleAttacks=["",""]
        for n in numtype:
            if n != "":
                c.execute(f"select identifier from moves where type_id='{n}'")
                pa=c.fetchall()
    
                for p in pa:
                    p=str(p).strip("(").strip(")").strip("'")
                    p=p[:-1]
                    p=p[:-1]
                    possibleAttacks.append(p)
        if movename in possibleAttacks:
            await ctx.send("You are trying to learn"+movename)
            c.execute(f"update ownedpokes set move{slotnumber}='{movename}' where owner={author} and id={pokeid}")
            conn.commit()
            c.close()
            await ctx.send(movename+" was learnt!")
        else:
            await ctx.send("Your pokemon cannot learn"+movename)
        await ctx.send("Selected Pokemon can learn moves with -learn <movename> <move slot>")
    @commands.command(name="moveset",aliases=['ms'])
    async def moveset(self, ctx):
        author=ctx.author.id
        authorpic=ctx.author.avatar_url
        conn=sqlite3.connect('/root/blazi/blaze/blazidb.db')

        c = conn.cursor()
        c.execute(f"select id from selected where owner='{author}'")
        num=c.fetchone()
        num=str(num).strip(",").strip(")").strip("(")

        num=num[:-1]

        c.execute(f"select Type from poke where number='{num}'")
        types=c.fetchone()
        types=str(types).strip(",").strip(")").strip("(")
        types=types[:-1]
        types=types[1:]
        fire=10
        steel=9
        ghost=8
        bug=7
        rock=6
        ground=5
        poison=4
        flying=3
        fighting=2
        water=11
        grass=12
        electric=13
        psychic=14
        ice=15
        dragon=16
        dark=17
        fairy=18
        normal=1
        typeinc=["",""]
        types=str(types).strip(",").strip(")").strip("(")
        types=types[:-1]
        if 'Fire' in types:
            typeinc.append('fire')
        if 'Water' in types:
            typeinc.append('water')
        if 'Grass' in types:
            typeinc.append('grass')
        if 'Bug' in types:
            typeinc.append('bug')
        if 'Flying' in types:
            typeinc.append('flying')
        if 'Dark' in types:
            typeinc.append('dark')
        if 'Psychic' in types:
            typeinc.append('psychic')
        if 'Ghost' in types:
            typeinc.append('ghost')
        if 'Fighting' in types:
            typeinc.append('fighting')
        if 'Ground' in types:
            typeinc.append('ground')
        if 'Rock' in types:
            typeinc.append('rock')
        if 'Steel' in types:
            typeinc.append('steel')
        if 'Normal' in types:
            typeinc.append('normal')
        if 'Fairy' in types:
            typeinc.append('fairy')
        if 'Poison' in types:
            typeinc.append('poison')
        if 'Dragon' in types:
            typeinc.append('dragon')
        if 'Ice' in types:
            typeinc.append('ice')
        if 'Electric' in types:
            typeinc.append('electric')
        if '' in types:
            typeinc.append('-')
        await ctx.send(str(typeinc))
        type1=str(typeinc[2])
        t2=" "
        t1=" "
        type2=str(typeinc[3])
        type1=str(type1).strip(",").strip(")").strip("(")
        numberselected=type1[:-1]
        
        type2=str(type2).strip(",").strip(")").strip("(")
        
        await ctx.send(type1)
        await ctx.send(type2)
        if (type1=='fire'):
            t1=fire
        elif (type1=='steel'):
            t1=steel
        elif (type1=='ghost'):
            t1=ghost
        elif (type1=='bug'):
            t1=bug
        elif (type1=='rock'):
            t1=rock
        elif (type1=='ground'):
            t1=ground
        elif (type1=='poison'):
            t1=poison
        elif (type1=='flying'):
            t1=flying
        elif (type1=='fighting'):
            t1=fighting
        elif (type1=='water'):
            t1=water
        elif (type1=='grass'):
            t1=grass
        elif (type1=='electric'):
            t1=electric
        elif (type1=='psychic'):
            t1=psychic
        elif (type1== 'ice'):
            t1=ice
        elif (type1=='dragon'):
            t1=dragon
        elif (type1=='dark'):
            t1=dark
        elif (type1=='fairy'):
            t1=fairy
        elif (type1=='normal'):
            t1=normal
        if (type2=='fire'):
            t2=fire
        elif (type2=='steel'):
            t2=steel
        elif (type2=='ghost'):
            t2=ghost
        elif (type2=='bug'):
            t2=bug
        elif (type2=='rock'):
            t2=rock
        elif (type2=='ground'):
            t2=ground
        elif (type2=='poison'):
            t2=poison
        elif (type2=='flying'):
            t2=flying
        elif (type2=='fighting'):
            t2=fighting
        elif (type2=='water'):
            t2=water
        elif (type2=='grass'):
            t2=grass
        elif (type2=='electric'):
            t2=electric
        elif (type2=='psychic'):
            t2=psychic
        elif (type2== 'ice'):
            t2=ice
        elif (type2=='dragon'):
            t2=dragon
        elif (type2=='dark'):
            t2=dark
        elif (type2=='fairy'):
            t2=fairy
        elif (type2=='normal'):
            t2=normal
            
        types=['-',t1,t2]
        mvst=["-","-"]
        message = await ctx.send("Populating movesets...")
        c.execute(f"select identifier from Moves where type_id='{t2}' or type_id='{t1}'")
        movese=c.fetchall()
        moves=['-','-']
        for m in movese:
            moves.append(m)
        moves="".join(str(moves))
        moves=moves.replace("',), ('","\n")
        moves=moves[13:-4]
        moves="```"+moves+"```"
        await ctx.send_interactive(pagify(moves))
    @commands.command(name="pokecenter",aliases=['heal'])
    async def pokecenter(self, ctx):
        await ctx.send('Welcome to the Pokecenter!')
    @commands.command(name="trade",aliases=['te'])
    async def trade(self, ctx,person:str):
        await ctx.send('trading')
    @checks.admin()
    @commands.command(name="check", aliases=['c'])
    async def check(self,ctx):
            await ctx.send("This is a check")
    @commands.command(name="n",aliases=['nm'])
    async def n(self, ctx,nk:str):
            author=ctx.author.id
            a=ctx.author
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"update adventure set nickname='{str(nk)}' where user='{author}'")
            conn.commit()
            c.close()
    @commands.command(name="infos",aliases=['is'])
    async def infos(infos, ctx,mpi:str):
            
            author=ctx.author.id
            authorpic=ctx.author.avatar_url
            if mpi=='c':
                    author=ctx.author.id
                    authorpic=ctx.author.avatar_url
                    conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                    c = conn.cursor()
                    c.execute(f"SELECT numbercaught FROM selected WHERE owner='{author}'")
                    selectednocaught=c.fetchone()
                    await ctx.send(selectednocaught)
                    numberselected=str(selectednocaught).strip(",").strip(")").strip("(")
                    numberselected=numberselected[:-1]
                    await ctx.send(numberselected)
                    c.execute(f"SELECT id FROM OwnedPokes WHERE owner='{author}' and numbercaught='{numberselected}'")
                    numc=c.fetchone()
                    numc=str(numc).strip(",").strip(")").strip("(").strip("'")
                    numc=numc[:-1]
                    c.execute(f"SELECT level FROM OwnedPokes WHERE owner='{author}' and numbercaught='{numberselected}'")
                    levelc=c.fetchone()
                    c.execute(f"SELECT hp FROM OwnedPokes WHERE owner='{author}'  and numbercaught='{numberselected}'")
                    hpc=c.fetchone()
                    c.execute(f"SELECT atk FROM OwnedPokes WHERE owner='{author}'  and numbercaught='{numberselected}'")
                    atkc=c.fetchone()
                    c.execute(f"SELECT def FROM OwnedPokes WHERE owner='{author}' and numbercaught='{numberselected}'")
                    dfc=c.fetchone()
                    c.execute(f"SELECT spatk FROM OwnedPokes WHERE owner='{author} 'and numbercaught='{numberselected}'")
                    satkc=c.fetchone()
                    c.execute(f"SELECT spdef FROM OwnedPokes WHERE owner='{author}' and numbercaught='{numberselected}'")
                    sdefc=c.fetchone()
                    c.execute(f"SELECT speed FROM OwnedPokes WHERE owner='{author}' and numbercaught='{numberselected}'")
                    sdc=c.fetchone()
                    c.execute(f"SELECT nickname  FROM OwnedPokes WHERE owner='{author}' and numbercaught='{int(numberselected)}'")

                    nick=c.fetchone()
                    nummc=str(numc)
                    numbc=str(nummc).strip(",").strip(")").strip("(").strip("'")
                    hpc=str(hpc)
                    hpc=str(hpc).strip(",").strip(")").strip("(").strip(\
"'")

                    hpc=hpc[:-1]
                    await ctx.send(hpc)
                    atkc=str(atkc)
                    atkc=str(atkc).strip(",").strip(")").strip("(").strip("'")
                    
                    atkcc=atkc[:-1]
                    dfc=str(dfc)
                    dfc=str(dfc).strip(",").strip(")").strip("(").strip(\
"'")
                    
                    dfc=dfc[:-1]
                    satkc=str(satkc)
                    satkc=str(satkc).strip(",").strip(")").strip("(").strip(\
"'")
                    
                    satkc=satkc[:-1]
                    sdefc=str(sdefc)
                    sdefc=str(sdefc).strip(",").strip(")").strip("(").strip(\
"'")
                    sdefc=sdefc[:-1]
                    sdc=str(sdc)
                    sdc=str(sdc).strip(",").strip(")").strip("(").strip(\
"'")
                    
                    sdc=sdc[1:]
                    totalc=0
                    totalc+=int(hpc)
                    totalc+=int(atkc)
                    totalc+=int(dfc)
                    totalc+=int(satkc)
                    totalc+=int(sdefc)
                    totalc+=int(sdc)
                    totalc=totalc*0.5376344086
                    await ctx.send(numbc)
                    chosen_imagec=f"http://pokepla.net/wp-content/uploads/2019/03/{str(numbc)}.png"
                    infoc=f"""```                                                                          
                    nickname:{str(nick)}
                    level:{str(levelc)}                                                                  
                  
                    hp:{hpc}                                                                             
                    attack:{atkc}                                                                        
                    defense:{dfc}                                                                        
                    special attack:{satkc}                                                               
                    '''"""
                    embed=discord.Embed()
                    embed.set_image(url=(chosen_imagec))
                    embed.description=f""" nickname:{str(nick)}                                     
                    level:{str(levelc)}                                     \
                                                                                                                                                        
                    hp:{hpc}                                                \
                                                                           
 
                    attack:{atkc}                                           \
                                                                             
                    defense:{dfc}                                           \
                                                                             
                    special attack:{satkc}                                  \
                                                                             
                    special defense:{sdefc}                                 \
                                                                             
                    speed:{sdc}
                    
                    TOTAL:{str(totalc)}%"""
                    
                    embed.set_thumbnail(url=authorpic)
                    await ctx.send(embed=embed)

            else:
                    
                    conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                    c = conn.cursor()
                    c.execute(f"SELECT id FROM OwnedPokes WHERE owner='{author}' and numbercaught='{mpi}'")
                    num=c.fetchone()
                    c.execute(f"SELECT level FROM OwnedPokes WHERE owner='{author}' and numbercaught='{int(mpi)}'")
                    level=c.fetchone()
                    c.execute(f"SELECT hp FROM OwnedPokes WHERE owner='{author}'  and numbercaught='{int(mpi)}'")
                    hp=c.fetchone()
                    c.execute(f"SELECT atk FROM OwnedPokes WHERE owner='{author}'  and numbercaught='{int(mpi)}'")
                    atk=c.fetchone()
                    c.execute(f"SELECT def FROM OwnedPokes WHERE owner='{author}' and numbercaught='{int(mpi)}'")
                    df=c.fetchone()
                    c.execute(f"SELECT spatk FROM OwnedPokes WHERE owner='{author} 'and numbercaught='{int(mpi)}'")
                    satk=c.fetchone()
                    c.execute(f"SELECT spdef FROM OwnedPokes WHERE owner='{author}' and numbercaught='{int(mpi)}'")
                    sdef=c.fetchone()
                    c.execute(f"SELECT speed FROM OwnedPokes WHERE owner='{author}' and numbercaught='{int(mpi)}'")
                    sd=c.fetchone()
                    numm=str(num)
                    numb=str(numm).strip(",").strip(")").strip("(").strip("'")
                    nu=numb[:-1]
                    level=str(level)
                    level=str(level).strip(",").strip(")").strip("(").strip("'")
                    level=level[:-1]

                    await ctx.send(nu)
                    c.execute(f"SELECT HP FROM poke WHERE number='{nu}'")
                    basehp=c.fetchone()
                    await ctx.send(basehp)
                    c.execute(f"SELECT Attack FROM poke WHERE number='{nu}'")
                    baseatk=c.fetchone()
                    c.execute(f"SELECT Defense FROM poke WHERE number='{nu}'")
                    basedef=c.fetchone()
                    c.execute(f"SELECT Sp_Atk FROM poke WHERE number='{nu}'")
                    basesatk=c.fetchone()
                    c.execute(f"SELECT Sp_Def FROM poke WHERE number='{nu}'")
                    basesdef=c.fetchone()
                    c.execute(f"SELECT Speed FROM poke WHERE number='{nu}'")
                    basesd=c.fetchone()
                    await ctx.send(basesd)
                    c.execute(f"SELECT nickname  FROM OwnedPokes WHERE owner='{author}' and numbercaught='{int(mpi)}'")

                    nick=c.fetchone()
                    basehp=str(basehp)
                    basehp=str(basehp).strip(",").strip(")").strip("(").strip("'")

                    basehp=basehp[:-1]
                    basehp=int(basehp)
                    baseatk=str(baseatk)
                    baseatk=str(baseatk).strip(",").strip(")").strip("(").strip\
("'")

                    baseatk=baseatk[:-1]
                    baseatk=int(baseatk)
                    basedef=str(basedef)
                    basedef=str(basedef).strip(",").strip(")").strip("(").strip\
("'")

                    basedef=basedef[:-1]
                    basedef=int(basedef)
                    basesatk=str(basesatk)
                    basesatk=str(basesatk).strip(",").strip(")").strip("(").strip\
("'")

                    basesatk=basesatk[:-1]
                    basesatk=int(basesatk)
                    basesdef=str(basesdef)
                    basesdef=str(basesdef).strip(",").strip(")").strip("(").strip\
("'")

                    basesdef=basesdef[:-1]
                    basesdef=int(basesdef)
                    basesd=str(basesd)
                    basesd=str(basesd).strip(",").strip(")").strip("(").strip\
("'")

                    basesd=basesd[:-1]
                    basesd=int(basesd)
                    hp=str(hp)
                    hp=str(hp).strip(",").strip(")").strip("(").strip("'")
                
                    
                    hp=hp[:-1]
                    atk=str(atk)
                    atk=str(atk).strip(",").strip(")").strip("(").strip("'")
                    
                    atk=atk[:-1]
                    df=str(df)
                    df=str(df).strip(",").strip(")").strip("(").strip(\
"'")
                    
                    df=df[:-1]
                    satk=str(satk)
                    satk=str(satk).strip(",").strip(")").strip("(").strip(\
"'")
                    
                    satk=satk[:-1]
                    sdef=str(sdef)
                    sdef=str(sdef).strip(",").strip(")").strip("(").strip(\
"'")
                    
                    sdef=sdef[:-1]
                    sd=str(sd)
                    sd=str(sd).strip(",").strip(")").strip("(").strip(\
"'")
                    sd=sd[:-1]
                    leve=int(level)
                    hpp=(int(basehp)*2+int(hp)+0)*(leve/100)+10+int(level)
                    atkp=(int(baseatk)*2+int(atk)+0)*(leve/100)+10
                    defp=(int(basedef)*2+int(df)+0)*(leve/100)+10
                    satkp=(int(basesatk)*2+int(satk)+0)*(leve/100)+10
                    sdefp=(int(basesdef)*2+int(sdef)+0)*(leve/100)+10
                    sdp=(int(basesd)*2+int(sd)+0)*(leve/100)+10
                    hpp=int(hpp)-5
                    atkp=int(atkp)-5
                    defp=int(defp)-5
                    satkp=int(satkp)-5
                    sdefp=int(sdefp)-5
                    sdp=int(sdp)-5
                    total=0
                    total+=int(hp)
                    total+=int(atk)
                    total+=int(df)
                    total+=int(satk)
                    total+=int(sdef)
                    total+=int(sd)
                    total=total*0.5376344086
                    chosen_image=f"http://pokepla.net/pokes//{str(nu)}.png"
                    info=f"""```
                    nickname:{str(nick)}
                    level:{str(level)}
                    hp:{hp}
                    attack:{atk}
                    defense:{df}
                    special attack:{satk}
                    special defense:{sdef}
                    speed:{sd}
                    Total:{total}%```"""
                    embed=discord.Embed()
                    embed.set_image(url=(chosen_image))
                    embed.description=f""" 
                    nickname:{str(nick)}                                                                                        
                    level:{str(level)}


                    hp:{hpp}  |   {hp}                                                                                                                             

                    attack:{atkp}    |       {atk}                                                                                                                        

                    defense:{defp}    |       {df}                                                                                                                        

                    special attack:{satkp}    |       {satk}                                                                                                               

                    special defense:{sdefp}    |       {sdef}                                                                                                              

                    speed:{sdp}    |       {sd}
                    
                    
                    Total:{total}%

                    """

                    embed.set_thumbnail(url=authorpic)
                    await ctx.send(embed=embed)
    @commands.command(name="party",aliases=['team'])
    async def party(self, ctx, partyfn:str, number:str):
        number.split("-")

        if(str(number[1])=="-"):
            caught=str(number[0])

            slot=str(number[2])
        elif(str(number[2])=="-"):
            caught=str(number[0]+number[1])

            slot=str(number[3])
            
        if "add" in partyfn:
        

            author=ctx.author.id
            await ctx.send("Add Pokemon with -party add <numbercaught> <partyslot>")
            await ctx.send(caught)
            await ctx.send(slot)

            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')

            c = conn.cursor()
            c.execute(f"delete from party where (owner='{author}'and PartySlot='{slot}')")
            conn.commit()
            c.execute(f"insert into party values('{author}','{caught}' ,'{slot}','None')")
            
            conn.commit()

            c.close()

        else:

            author=ctx.author.id

            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')

            c = conn.cursor()

            c.execute(f"Select numbercaught from party where owner='{author}' and PartySlot='1'")

            slot1=c.fetchone()

            c.execute(f"Select numbercaught from party where owner='{author}' and PartySlot='2'")

            slot2=c.fetchone()

            c.execute(f"Select numbercaught from party where owner='{author}' and PartySlot='3'")

            slot3=c.fetchone()

            c.execute(f"Select numbercaught from party where owner='{author}' and PartySlot='4'")

            slot4=c.fetchone()

            c.execute(f"Select numbercaught from party where owner='{author}' and PartySlot='5'")

            slot5=c.fetchone()

            c.execute(f"Select numbercaught from party where owner='{author}' and PartySlot='6'")

            slot6=c.fetchone()

            slot1=str(slot1).strip("(").strip("'").strip(",").strip(")")
            slot1=slot1[:-2]
            slot2=str(slot2).strip("(").strip("'").strip(",").strip(")")
            slot2=slot2[:-2]

            slot3=str(slot3).strip("(").strip("'").strip(",").strip(")")
            slot3=slot3[:-2]

            slot4=str(slot4).strip("(").strip("'").strip(",").strip(")")
            slot4=slot4[:-2]

            slot5=str(slot5).strip("(").strip("'").strip(",").strip(")")
            slot5=slot5[:-2]

            slot6=str(slot6).strip("(").strip("'").strip(",").strip(")")
            slot6=slot6[:-2]
            c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{slot1}'")
            one=c.fetchone()
            c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{slot2}'")
            two=c.fetchone()
            c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{slot3}'")
            three=c.fetchone()
            c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{slot4}'")
            four=c.fetchone()
            c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{slot5}'")
            five=c.fetchone()
            c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{slot6}'")
            six=c.fetchone()
            one=str(one).strip("(").strip("'").strip(",").strip(")")
            one=one[:-1]
            two=str(two).strip("(").strip("'").strip(",").strip(")")
            two=two[:-1]

            three=str(three).strip("(").strip("'").strip(",").strip(")")
            three=three[:-1]

            four=str(four).strip("(").strip("'").strip(",").strip(")")
            four=four[:-1]

            five=str(five).strip("(").strip("'").strip(",").strip(")")
            five=five[:-1]

            six=str(six).strip("(").strip("'").strip(",").strip(")")
            six=six[:-1]
            c.execute(f"Select Name from poke where number='{one}'")
            on=c.fetchone()
            c.execute(f"Select Name from poke where number='{two}'")
            tw=c.fetchone()
            c.execute(f"Select Name from poke where number='{three}'")
            thr=c.fetchone()
            c.execute(f"Select Name from poke where number='{four}'")
            fou=c.fetchone()
            c.execute(f"Select Name from poke where number='{five}'")
            fiv=c.fetchone()
            c.execute(f"Select Name from poke where number='{six}'")
            si=c.fetchone()
            on=str(on).strip("(").strip("'").strip(",").strip(")")
            on=on[:-2]
            tw=str(tw).strip("(").strip("'").strip(",").strip(")")
            tw=tw[:-2]
            thr=str(thr).strip("(").strip("'").strip(",").strip(")")
            thr=thr[:-2]

            fou=str(fou).strip("(").strip("'").strip(",").strip(")")
            fou=fou[:-2]

            fiv=str(fiv).strip("(").strip("'").strip(",").strip(")")
            fiv=fiv[:-2]

            si=str(si).strip("(").strip("'").strip(",").strip(")")
            si=si[:-2]
            await ctx.send("This will be your Party!")

            partyinfo=f"""```
            
            ----------------                  
            | {on} | {tw} |
            ----------------
            |{thr}| {fou}|
            ----------------
            {fiv} | {si} |
            ----------------
            ``` """
            await ctx.send(partyinfo)
    @commands.command(name="letsgo",aliases=['beginadventure'])
    @givec(amount=300)
    async def letsgo(self, ctx):
        authorcmd=ctx.message.author.id
        await ctx.send("```Ready to start the adventure!```")
        e = discord.Embed(title="oak", description="intro")
        e.set_image(url="https://em.wattpad.com/a6d4df2d1d37d6e11ffff7b1c92bef35960e1e67/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f46466171655642547367566838773d3d2d3630393539303139382e313534353135626336323332396237353731313435363631323134362e676966?s=fit&w=720&h=720")
        await ctx.send("https://zippy.gfycat.com/EarlyVacantAmurratsnake.webm")
        regionpick=("```Please Select a region!```")
        await ctx.send(regionpick)
        starters=[""]
        response = await self.bot.wait_for("message",timeout=600)
        
        if response.content.casefold().capitalize()=="Kanto":
            starters=["Charmander","Squirtle","Bulbasaur"]
        elif response.content.casefold().capitalize()=="Johto":
            starters=["Cyndaquil","Totodile","chikorita"]
        elif response.content.casefold().capitalize()=="Hoenn":
            starters=["Torchic","Mudkip","Treecko"]
        elif response.content.casefold().capitalize()=="Sinnoh":
            starters=["Chimchar","Piplup","Turtwig"]
        elif response.content.casefold().capitalize()=="Unova":
            starters=["Tepig","Oshawott","Snivy"]
        elif response.content.casefold().capitalize()=="Kalos":
            starters=["Fennekin","Froakie","Chespin"]
        elif response.content.casefold().capitalize()=="Alola":
            starters=["Litten","Popplio","Rowlet"]
        else:
            await ctx.send("```Please pick a valid region!```")
        global pickedpokestarter    
        await ctx.send(f"```Would you like {starters[0]} ,{starters[1]} or {starters[2]}```")
        author=str(response.author.id)
        pickedpokestarter = await self.bot.wait_for("message",timeout=300)
        randlevel=5
        randhp=rand.randint(0,31)
        randatk=rand.randint(0,31)
        randdef=rand.randint(0,31)
        randsp_atk=rand.randint(0,31)
        randsp_def=rand.randint(0,31)
        randsp=rand.randint(0,31)
        if(pickedpokestarter.content.casefold().capitalize() in starters):
            await ctx.send("```Congratulations! "+pickedpokestarter.content.lower().capitalize()+" is your first Pokemon!```")
            startpokes=pickedpokestarter.content.lower().capitalize()
            spoke=str(startpokes)
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
            numberofpokes=c.fetchall()
            noofpokes=len(numberofpokes)
            newnumberofpokes=noofpokes+1
            ctx.send(noofpokes)
            c.execute("INSERT into Profile VALUES("+author+",'None',0,0,'initiate','None')")
            conn.commit()
            c.close()
            c=conn.cursor()
            c.execute(f"Select number from poke where Name='{spoke}'")
            pokeNumber=c.fetchone()
            pokeNumber=str(pokeNumber).strip(",").strip(")").strip("(").strip("')").strip("'")
            pokeNumber=pokeNumber[:-1]
            pokeNum=int(pokeNumber)
            c.close()
            c = conn.cursor()
            itemdrop='None'
            c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),pokeNum,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
            conn.commit()
            c.execute(f"insert into adventure(user,energy) values({str(author)},10)")
            conn.commit()
            c.close()
            await ctx.send("```Setting up your profile!```")
        else:
            await ctx.send("```Try Again! Professor Oak does not have that Pokemon here!```")
    @commands.command(name="nickp",aliases=['np'])
    async def nickp(self, ctx,num:int, name:str):
        author=ctx.author.id
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute(f"update ownedpokes set nickname='{name}' where owner='{author}' and numbercaught='{num}'")
        conn.commit()
        c.close()
    @commands.command(name="me",aliases=['bnc'])
    async def me(self, ctx):
        authorpic=ctx.author.avatar_url
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        author=str(ctx.message.author.id)
        c = conn.cursor()
        c.execute(f"SELECT badges from Profile where user_name='{author}'")
        badges=c.fetchone()
        c.execute(f"SELECT balance from Profile where user_name='{author}'")
        credit=c.fetchone()
        c.execute(f"SELECT redeems from Profile where user_name='{author}'")
        deems=c.fetchone()
        c.execute(f"SELECT role from Profile where user_name='{author}'")
        roles=c.fetchone()
        c.close()
        c=conn.cursor()
        c.execute(f"select numbercaught from OwnedPokes where owner='{author}'")
        nopokes=c.fetchall()
        c.execute(f"SELECT energy from adventure where user='{author}'")
        energy=c.fetchone()
        c.execute(f"SELECT nickname from adventure where user='{author}'")
        nm=c.fetchone()
        if(nm==None):
                name=author
        else:
                name=nm
        npokeprf=len(nopokes)+1
        profilestuffs=f"""```
        Trainer Profile
        Nickname:{name}"
        Number of Pokes:{npokeprf}
        Redeems:{str(deems)}
        "Roles:{str(roles)}
        "Badges:{str(badges)}
        "Credits:{str(credit)}```"""
        embed=discord.Embed()
        embed.description=f""" nickname:{str(name)}             
        
        Number of Pokes:{npokeprf}                                       
        
        
        Redeems:{(deems)}                                                 
        
        
        Roles:{str(roles)}                                            
        
        
        Badges:{str(badges)}
        """
        
        embed.set_thumbnail(url=authorpic)
        await ctx.send(embed=embed)
        
    async def on_message(self, message):

        author=message.author
        self.count=self.count+1
        if(self.count %1==0):
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"select id from selected where owner='{author.id}'")
            selectedinfos=c.fetchone()
            sid=str(selectedinfos)
            sid=str(sid).strip("(").strip("'").strip(",")
            sid=sid[:-1]
            sid=sid[:-1]
            print(sid)
            sidlen=len(sid)
            if(sidlen==1):
                sid='00'+sid
            elif(sidlen==2):
                sid='0'+sid
            else:
                print('correct length')
                print(sid)
            c.execute(f"select numbercaught from selected where owner='{author.id}'")
            selectedinfosf=c.fetchone()
            snc=str(selectedinfosf)
            snc=str(snc).strip("(").strip("'").strip(",")
            snc=snc[:-1]
            snc=snc[:-1]
            print(snc)
            c.execute(f"select level from ownedpokes where id='{sid}' and numbercaught='{snc}' and owner='{author.id}'")
            pinfosl=c.fetchone()
            lvl=str(pinfosl)
            lvl=str(lvl).strip("(").strip("'").strip(",")
            lvl=lvl[:-1]
            lvl=lvl[:-1]
            print(lvl+'level')
            c.execute(f"select exp from ownedpokes where id='{sid}' and numbercaught='{snc}' and owner='{author.id}'")
            pinfosx=c.fetchone()
            xp=str(pinfosx)
            xp=str(xp).strip("(").strip("'").strip(",")
            xp=xp[:-1]
            xp=xp[:-1]
            c.execute(f"select evolution_trigger_id from xpstuff where minimum_level='{lvl}' ")
            xpmr=c.fetchone()
            exp=str(xpmr)
            c.execute(f"select experience from evolutionxp  where level='{lvl}' ")
            xpmx=c.fetchone()
            txp=str(xpmx)
            txp=txp[:-1]
            txp=txp[:-1]
            txp=txp[1:]
            exp=str(exp).strip("(").strip("'").strip(",")
            txp=str(txp).strip("(").strip("'").strip(",")
            exp=exp[:-1]
            exp=exp[:-1]
            print("current exp"+xp)
            xpgain=int(lvl)*int(lvl)*int(lvl)
            xpgain=xpgain-int(lvl)
            xpgain=xpgain/5
            print("gained"+str(xpgain))
            xpset=int(xpgain)+int(xp)
            print('total xp'+str(xpset))
            c.execute(f"update ownedpokes set exp={str(xpset)} where owner={author.id} and id={sid} and numbercaught={snc}")
            conn.commit()
            xpt=int(xpset)
            print(str(xpt)+'total xp')
            print(exp+'gained')
            print(xpt)
            print(txp)
            if int(xpt) >= int(txp):
                level=int(lvl)+1
                c.execute(f"update ownedpokes set level={level}, exp='0'  where owner={author.id} and id={sid} and numbercaught={snc}")
                conn.commit()
            else:
                print('not yet')
            c.execute(f"select exp from ownedpokes where owner='{author.id}' and id='{sid}' and numbercaught='{snc}'")
            level=c.fetchone()
            level=str(level).strip("(").strip("'").strip(",")
            print(level)
            dis=sid
            sid='#'+sid
            
            xid=str(sid)
            
            c.execute(f"select level from evos where id='{xid}';")
            minevo=c.fetchone()
            minevo=str(minevo)[:-1]
            minevo=minevo[1:-1]
            print(minevo+'evo level')
            if "o" in minevo:
                print('No evolution')
            if minevo.isdigit()==False:
                print('nope')
                
            elif(int(lvl)>=int(minevo)):
                pid=0
                idp=sid[1:]
                pid=int(idp)+1
                c.execute(f"update ownedpokes set id={pid} where owner={author.id} and id={dis} and numbercaught={snc}")
                conn.commit()
                c.execute(f"select Name from poke where number='{pid}'")
                name=c.fetchall()
                name=str(name)
                await message.channel.send(f"your pokemon evolved into {name}")
                c.close()
            else:
                print("hi")
            
        if(self.count %25==0 or self.count %35==0):
               spawned=rand.randint(1,807)
               if len(str(spawned))==1:
                   spawned="00"+str(spawned)
               elif len(str(spawned))==2:
                   spawned="0"+str(spawned)
               shiny=rand.randint(0,100)
               if spawned in [19,20,26,27,28,29,37,38,50,51,52,53,74,75,76,88,89,103,105]:
                   randalola=rand.randint(0,4)
                   if randalola==0:
                       spawned=spawned+'_61'
  
               conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
               c = conn.cursor()
               await message.channel.send("```Say the  Poke Name to catch it!and throw a Ball!```")
               if shiny==50:
                   spawnshiny=str(spawned)+"_Shiny"

               spawnshiny=str(spawned)
               chosen_image="http://pokepla.net/pokes/"+spawnshiny+".png"
               pokemonimagesend=(await message.channel.send(chosen_image))
               c.execute(f"SELECT Name FROM poke WHERE number={spawned}")
               randName=c.fetchone()
               randompoke=(", ".join(randName))
               c.close()
               spawnedno=int(spawned)
               catchtry = await self.bot.wait_for("message",timeout=300)
               tries=0
               while catchtry.content.casefold().capitalize() != randompoke and tries<6:
                   catchtry = await self.bot.wait_for("message",timeout=300)
                   tries=tries+1
                   
               if(catchtry.content.casefold().capitalize() == randompoke):
                       await message.channel.send("```You throw a ball at the  "+randompoke+"!```")
                       conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                       c = conn.cursor()
                       
                       # reaction = await self.bot.wait_for(':emoji_8:'))

                       #await ctx.send(f"You responded with {reaction} ")
                       randlevel=rand.randint(1,70)
                       randhp=rand.randint(0,31)
                       randatk=rand.randint(0,31)
                       randdef=rand.randint(0,31)
                       randsp_atk=rand.randint(0,31)
                       randsp_def=rand.randint(0,31)
                       randsp=rand.randint(0,31)
                       author=str(catchtry.author.id)
                       c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                       numberofpokes=c.fetchall()
                       noofpokes=len(numberofpokes)
                       newnumberofpokes=noofpokes+1
                       c.close()
                       c=conn.cursor()
                       itemdrop='None'
                       c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(catchtry.author.id),spawnedno,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))

                       conn.commit()
                       c.close()
               else:
                       await message.channel.send(randompoke+" ran away!")
                       caught='ranaway'
        elif(self.count %45==0):
            randnpc=["Beauty","Biker","Blackbelt","Bug Catcher","Engineer","Fisherman","Gambler","Hiker","Juggler","Youngster","Lass","Pokefan","Psychic","Sailor","Scientist","Firebreather","Kimono Girl","Medium","Officer","Skier","Dragon Tamer","Pokemon Breeder","Expert","Pokemon Ranger","Baker","Doctor","Ace"]
            namesofnpc=['Joey','Martin','Jay','Jonah','Jessica','Albert','Bianca','Danielle','Mary','Kirito-kun', 'Asuna-Chan','Pheobe','Ichigo','Rukia','Chad','Goku','Vegeta' ]
            
            npc=rand.choice(randnpc)+rand.choice(namesofnpc)
            await message.channel.send(npc+" wants to battle!")
            self.count==0
    @commands.command(name="select",aliases=['sp'])
    async def select(self, ctx,numberselect:str):
           author=str(ctx.message.author.id)
           selected=""
           conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
           c = conn.cursor()
           c.execute(f"Select id from OwnedPokes where owner='{author}' and numbercaught='{numberselect}'")
           selectedpokenam=c.fetchone()
           c.execute(f"delete from selected where owner='{author}'")
           conn.commit()
           selectedpokename=str(selectedpokenam)
           selectedpokename=selectedpokename.strip(")").strip("(").strip(",")
           c.close()
           c = conn.cursor()
           pokemonnameselect=c.fetchone()
           pokemonnameselect=str(pokemonnameselect).strip("(").strip("'").strip(",")
           conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
           c = conn.cursor()
           c.execute(f"Select Name from poke where number='{selectedpokename}'")
           pokemonnameselect=c.fetchone()
           pokemonnameselect=str(pokemonnameselect).strip("(").strip("'").strip(",")
           pokemonnameselect=pokemonnameselect[:-1]
           pokemonnameselect=pokemonnameselect[:-1]
           pokemonnameselect=pokemonnameselect[:-1]
           c.execute(f"Insert into selected values('{author}','{numberselect}','{selectedpokename}')")
           conn.commit()
           c.close()
           await ctx.send("You have selected your "+str(pokemonnameselect))
           
           
           
    @commands.command(name="pokes",aliases=['pm'])
    async def pokes(self, ctx):
            author=str(ctx.message.author.id)
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"Select id  from OwnedPokes where owner='{author}'")
            pokescaughtlist=c.fetchall()
            
            if pokescaughtlist== None:
                    await ctx.send("You have no pokemon!")
            embed = discord.Embed(title="Caught Pokemon")        
            pli=["-","-"]
            pokename=['-','-']
            for r in pokescaughtlist:
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                c.execute(f"select id from OwnedPokes where id='{r[0]}' and owner='{author}'")
                      
                pokenum=c.fetchall()
                for n in pokenum:
                    n=str(n).strip("(").strip(")").strip(",")
                    c.execute(f"select Name from poke where number='{n}'")
                    pokenames=c.fetchall()
                    for p in pokenames:
                        pokename.append(p)
                    pokename="".join(str(pokename))
                    pokename=pokename.replace("',), ('","\n")
                    pokename=pokename[13:-4]
                    pokename="```"+pokename+"```"
                    await ctx.send_interactive(pagify(pokename))
    @commands.command(name="infop",aliases=['i'])
    async def infop(self, ctx, pokechosen:str):
            if("Mega" in pokechosen):
                    mpoke=pokechosen.split('-')
                    mpname=str(mpoke[1])
                    conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                    c = conn.cursor()
                    c.execute(f"select number from poke where Name='{mpname}'")
                    mpchosennum=c.fetchone()
                    c.close()
                    mp=str(mpchosennum).strip("(").strip(")").strip(",")
                    await ctx.send(mp)
                    await ctx.send("http://pokepla.net/pokes/"+str(mp)+"-mega.png")       
            elif("Shiny" in pokechosen):
                mpoke=pokechosen.split('-')
                mpname=str(mpoke[1])
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                c.execute(f"select number from poke where Name='{mpname}'")
                mpchosennum=c.fetchone()
                c.close()
                mp=str(mpchosennum).strip("(").strip(")").strip(",")
                await ctx.send(mp)
                mpl=len(mp)
                if(mpl==1):
                    mp="00"+mp
                elif(mpl==2):
                    mp="0"+mp
                await ctx.send("http://pokepla.net/pokes/"+str(mp)+"_shiny.png")
            elif("alo" in pokechosen):
                mpoke=pokechosen.split('-')
                mpname=str(mpoke[1])
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                c.execute(f"select number from poke where Name='{mpname}'")
                mpchosennum=c.fetchone()
                c.close()
                mp=str(mpchosennum).strip("(").strip(")").strip(",")
                await ctx.send(mp)
                mpl=len(mp)
                if(mpl==1):
                    mp="00"+mp
                elif(mpl==2):
                    mp="0"+mp
                await ctx.send("http://pokepla.net/pokes/"+str(mp)+"_61.png")


            else:
                    if(pokechosen.isdigit()):

                        
                            if(len(pokechosen)==1):
                                pokechosen="00"+pokechosen
                            elif(len(pokechosen)==2):
                                pokechosen=="0"+pokechosen
                            await ctx.send("http://pokepla.net/pokes/"+str(pokechosen)+".png")
                            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                            c = conn.cursor()
                            c.execute(f"select HP from poke where number='{pokechosen}'")
                            pokehp=c.fetchone()
                            c.execute(f"select Attack from poke where number='{pokechosen}'")
                            pokeatk=c.fetchone()
                            c.execute(f"select Defense from poke where number='{pokechosen}'")
                            pokedef=c.fetchone()
                            c.execute(f"select Sp_Atk from poke where number='{pokechosen}'")
                            pokespatk=c.fetchone()
                            c.execute(f"select Sp_Def from poke where number='{pokechosen}'")
                            pokespdef=c.fetchone()
                            c.execute(f"select Speed from poke where number='{pokechosen}'")
                            Speed=c.fetchone()
                            pokehp=str(pokehp)
                            pokeatk=str(pokeatk)
                            pokedef=str(pokedef)
                            pokespatk=str(pokespatk)
                            pokespdef=str(pokespdef)
                            Speed=str(Speed)
                            stats=f"""                                                                    
                                   ```
                                       Attack: {pokeatk}                                                  
                                       Defense: {pokedef}                                                 
                                       Special Attack: {pokespatk}                                        
                                       Special Defense: {pokespdef}                                       
                                       Speed: {Speed}```"""
                            await ctx.send(stats)
                    else:
                            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                            c = conn.cursor()
                            c.execute(f"select number from poke where Name='{pokechosen}'")
                            pokechosennumber=c.fetchone()
                            c.execute(f"select HP from poke where Name='{pokechosen}'")
                            pokehp=c.fetchone()
                            c.execute(f"select Attack from poke where Name='{pokechosen}'")
                            pokeatk=c.fetchone()
                            c.execute(f"select Defense from poke where Name='{pokechosen}'")
                            pokedef=c.fetchone()
                            c.execute(f"select Sp_Atk from poke where Name='{pokechosen}'")
                            pokespatk=c.fetchone()
                            c.execute(f"select Sp_Def from poke where Name='{pokechosen}'")
                            pokespdef=c.fetchone()
                            c.execute(f"select Speed from poke where Name='{pokechosen}'")
                            Speed=c.fetchone()
                            pokehp=str(pokehp)
                            pokeatk=str(pokeatk)
                            pokedef=str(pokedef)
                            pokespatk=str(pokespatk)
                            pokespdef=str(pokespdef)
                            Speed=str(Speed)
                        
                            chosendig=str(pokechosennumber).strip("(").strip(")").strip(",")
                            if len(chosendig)==1:
                                chosendig="00"+chosendig
                            elif len(chosendig)==2:
                                chosendig="0"+chosendig
                            await ctx.send("http://pokepla.net/pokes/"+str(chosendig)+".png")
                            stats=f"""
                                   ``` Attack: {pokeatk}
                                       Defense: {pokedef}
                                       Special Attack: {pokespatk}
                                       Special Defense: {pokespdef}
                                       Speed: {Speed}```"""
                            await ctx.send(stats)
                            c.close()
    @commands.command(name="breed",aliases=['brd'])
    async def breed(self, ctx):
        await ctx.send("Breeding")
    @commands.command(name="fish",aliases=['fs'])
    @charge(amount=100)
    async def fish(self, ctx):
        authorf=ctx.message.author.id
        await ctx.send("```Let's go Fish!```")
        await ctx.send("http://pokepla.net/wp-content/uploads/2019/03/3c3aa2543f7ba3986cf780e3c0ac772e.jpg")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Water' or Type='Ice'")
        waterpokes=c.fetchall()
        waterspawn= rand.choice(waterpokes)
        water=str(waterspawn)
        water=water.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(water)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{water}'")
        waterpokename=c.fetchone()
        
        wpoke=str(waterpokename)
        wpoke=wpoke.strip("(").strip(")").strip("'").strip("'").strip(",")
        wpoke=wpoke[:-1]
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+str(water)+".png"
        await ctx.send(chosen_image)

        await ctx.send("```Oh! There's a bite! Say the Pokemon's name to  catch it!```")
        fishingcatch = await self.bot.wait_for("message",timeout=900)
        authorp=fishingcatch.author.id
        while authorp != ctx.message.author.id and fishingcatch.content.casefold().capitalize() !=wpoke:
                x =1
        if(authorp==authorf):
                if(fishingcatch.content.casefold().capitalize() ==wpoke):
                        self.count=0
                        await ctx.send("```You caught the "+str(fishingcatch.content)+"!```")
                        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                        c = conn.cursor()
                        randlevel=rand.randint(1,70)
                        randhp=rand.randint(0,31)
                        randatk=rand.randint(0,31)
                        randdef=rand.randint(0,31)
                        randsp_atk=rand.randint(0,31)
                        randsp_def=rand.randint(0,31)
                        randsp=rand.randint(0,31)
                        author=str(fishingcatch.author.id)
                        c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                        numberofpokes=c.fetchall()
                        noofpokes=len(numberofpokes)
                        newnumberofpokes=noofpokes+1
                        c.close()
                        c=conn.cursor()
                        itemdrop='None'
                        c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),water,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                        conn.commit()
                        c.close()
                else:
                        await ctx.send("```It swam  away!```")
                        
    @commands.command(name="haunt",aliases=['h'])
    @charge(amount=100)
    async def haunt(self, ctx):
            await ctx.send("```Haunting time!```")
            await ctx.send("https://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-omega-ruby\-and-alpha-sapphire/8/88/Orasw915orasw916.png?width=640")
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute("SELECT number FROM poke WHERE Type = 'Ghost' or  Type like '%Ghost' or Type like 'Ghost%'")
            ppokes=c.fetchall()
            pspawn= rand.choice(ppokes)
            pight=str(pspawn)
            pight=pight.strip("(").strip(")").strip(",")
            chosen_image ="http://pokepla.net/pokes/"+str(pight)+".png"
            c.execute(f"SELECT Name FROM poke WHERE number='{pight}'")
            ppokename=c.fetchone()

            ppoke=str(ppokename)
            ppoke=ppoke.strip("(").strip(")").strip("'").strip("'").strip(",")
            ppoke=ppoke[:-1]
            print(ppoke)
            print(pight)
            if 'alo' in ppoke:
                pight=pight+'_61'
            else:
                print('not alolan')
            chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+pight+".png"
            await ctx.send(chosen_image)
            await ctx.send("```Oh! A pokemon came to haunt you!  Say the Pokemon's name to  catch\
 it!```")
            pightcatch = await self.bot.wait_for("message",timeout=1900)
            if(pightcatch.content.casefold().capitalize() ==ppoke):
                    self.count=0
                    await ctx.send("```You caught the "+str(pightcatch.content)+"!```")
                    conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                    c = conn.cursor()
                    randlevel=rand.randint(1,70)
                    randhp=rand.randint(0,31)
                    randatk=rand.randint(0,31)
                    randdef=rand.randint(0,31)
                    randsp_atk=rand.randint(0,31)
                    randsp_def=rand.randint(0,31)
                    randsp=rand.randint(0,31)
                    author=str(pightcatch.author.id)
                    c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                    numberofpokes=c.fetchall()
                    noofpokes=len(numberofpokes)
                    newnumberofpokes=noofpokes+1
                    c.close()
                    c=conn.cursor()
                    itemdrop='None'
                    c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),pight,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                    conn.commit()
                    c.close()
            else:

                            await ctx.send("```It went to haunt with someone else!```")

    @commands.command(name="train",aliases=['tn'])
    @charge(amount=100)
    async def train(self, ctx):
            await ctx.send("```Let's go Train!```")
            await ctx.send("https://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-omega-ruby\-and-alpha-sapphire/8/88/Orasw915orasw916.png?width=640")
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute("SELECT number FROM poke WHERE Type = 'Fighting' or  Type like '%Fighting' or type like 'Fighting%' or Type = 'Normal' or  Type like '%Normal' or type like 'Normal%'")
            fpokes=c.fetchall()
            fspawn= rand.choice(fpokes)
            fight=str(fspawn)
            fight=fight.strip("(").strip(")").strip(",")
            chosen_image ="http://pokepla.net/wp-content/uploads/photo-gallery/imported_from_med\ia_libray/"+str(fight)+".png"
            c.execute(f"SELECT Name FROM poke WHERE number='{fight}'")
            fpokename=c.fetchone()
            
            fpoke=str(fpokename)
            fpoke=fpoke.strip("(").strip(")").strip("'").strip("'").strip(",")
            fpoke=fpoke[:-1]
            chosen_image ="http://pokepla.net/pokes/"+fight+".png"
            await ctx.send(chosen_image)
            await ctx.send("```Oh! A pokemon came to spar!  Say the Pokemon's name to  catch it!```")
            fightcatch = await self.bot.wait_for("message",timeout=1900)
            if(fightcatch.content.casefold().capitalize() ==fpoke):
                    self.count=0
                    await ctx.send("```You caught the "+str(fightcatch.content)+"!```")
                    conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                    c = conn.cursor()
                    randlevel=rand.randint(1,70)
                    randhp=rand.randint(0,31)
                    randatk=rand.randint(0,31)
                    randdef=rand.randint(0,31)
                    randsp_atk=rand.randint(0,31)
                    randsp_def=rand.randint(0,31)
                    randsp=rand.randint(0,31)
                    author=str(fightcatch.author.id)
                    c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                    numberofpokes=c.fetchall()
                    noofpokes=len(numberofpokes)
                    newnumberofpokes=noofpokes+1
                    c.close()
                    c=conn.cursor()
                    itemdrop='None'
                    c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),fight,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                    conn.commit()
                    c.close()
            else:
                    await ctx.send("```It went to spar with someone else!```")
    @commands.command(name="mining",aliases=['mn'])
    @charge(amount=100)
    async def mining(self, ctx):
        await ctx.send("```Let's go Mining!```")
        await ctx.send("https://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-omega-ruby-and-alpha-sapphire/8/88/Orasw915orasw916.png?width=640")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Ground'or Type='Steel'  or Type='Rock'or  Type like '%Ground' or type like 'Ground%' or  Type like '%Rock' or type like 'Rock%'or  Type like '%Steel' or type like 'Steel%'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke.strip("(").strip(")").strip("'").strip("'").strip(",")
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A pokemon dug its way up!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
                await ctx.send("```It dug away!```")
    @commands.command(name="duel",aliases=['d'])
    async def duel(self, ctx,opponent:discord.Member):
        Challenger1=ctx.author.id
        Challenger2=opponent
        await ctx.send(str(Challenger2.mention)+" ! "+ctx.author.mention+" has challenged you to a duel!")
        await ctx.send('say Accept or Decline')
        response = await self.bot.wait_for("message", timeout=600)
        if(response.author.id==opponent.id and response.content.casefold().capitalize()=='Accept'):
            await ctx.send("http://31.media.tumblr.com/458d04b673d81a1a6f2c3dfc335101b8/tumblr_mhw8j5ypzD1rsc51fo1_500.gif")
            a='accepted'
            c2=Challenger2.id
            c1=Challenger1
            conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
            c = conn.cursor()
            c.execute(f"select id from selected where owner='{c1}'")
            c1id=c.fetchone()
            c1id=str(c1id).strip("(").strip(")").strip("'").strip(",")
            await ctx.send(c1id)
            c.execute(f"select id from selected where owner='{c2}'")
            c2id=c.fetchone()
            c2id=str(c2id).strip("(").strip(")").strip("'").strip(",")
            await ctx.send(c2id)
            c.execute(f"select Name from poke where number='{c1id}'")
            c1pokename=c.fetchone()
            c.execute(f"select Name from poke where number='{c2id}'")
            c2pokename=c.fetchone()
            await ctx.send(str(c1pokename)+" vs "+str(c2pokename))
            await ctx.send('working on images for this')
            await ctx.send('Preparing for battle...')
            c.execute(f"select HP,Attack,Defense,Sp_Atk,Sp_Def,Speed from poke where number='{c1id}'")
            c1stats=c.fetchall()
            c.execute(f"select HP,Attack,Defense,Sp_Atk,Sp_Def,Speed from poke where number='{c2id}'")
            c2stats=c.fetchall()
            c.execute(f"select hp,atk,def,spatk,spdef,speed from ownedpokes where id='{c1id}' and owner='{Challenger1}'")
            c1ivs=c.fetchall()
            c.execute(f"select hp,atk,def,spatk,spdef,speed from ownedpokes where id='{str(c2id)}' and owner='{c2}'")
            c2ivs=c.fetchall()
            await ctx.send('almost there')
        elif(response.content.casefold().capitalize=='Decline'):
            await ctx.send("Duel has been cancelled")
        else:
            print('none')
    @commands.command(name="battle",aliases=['fight'])
    async def battle(self, ctx):
        await ctx.send("6v6 battle")
        
    @commands.command(name="dragon",aliases=['dt'])
    @charge(amount=100)
    async def dragon(self, ctx):
        await ctx.send("```Let's go hunting for Dragons!```")
        await ctx.send("https://media.discordapp.net/attachments/552697721543196682/560324719396651014/cd219a9a5ebc4aafde21cdc73b341a13e82dd55b_hq.jpg")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Dragon 'or Type like '%Dragon' or Type like 'Dragon%'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke.strip("(").strip(")").strip("'").strip("'").strip(",")
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Dragon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
                await ctx.send("```It went to take a nap!```")
    @commands.command(name="thunderdome",aliases=['td'])
    @charge(amount=100)
    async def thunderdome(self, ctx):
        await ctx.send("```Let's go to the ThunderDome!```")
        await ctx.send("http://fc03.deviantart.net/fs70/f/2012/061/d/d/electric_pokemon_background_by_chancethewolf1282-d4rjfkq.png")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Electric 'or Type like '%Electric' or Type like 'Electric%'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke.strip("(").strip(")").strip("'").strip("'").strip(",")
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Pokemon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
            await ctx.send("```It went to  Recharge!```")
    @checks.admin()
    @commands.command(name="kenseionly",aliases=['ko'])
    async def kenseionly(self, ctx,v:str):
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute(f"SELECT Name FROM poke WHERE number='{v}'")
        gpokes=c.fetchone()
        Ground=str(gpokes)
        Ground=Ground.strip("(").strip(")").strip(",")
        Ground=Ground[:-1]
        Ground=Ground[1:]
        chosen_image ="http://pokepla.net/wp-content/uploads/photo-gallery/imported_from_media_libray/"+str(v)+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Pokemon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        await ctx.send(str(Ground))
        if(miningcatch.content.casefold().capitalize() ==str(Ground).casefold().capitalize()):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle', 'Tackle' , 'Tackle' ,'Tackle')",(str(author),v,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
                await ctx.send("```It went to take a nap!```")
    @commands.command(name='fortune',alias='fne')
    @charge(amount=100)
    async def fortune(self, ctx):
        await ctx.send("```Let's go to the fortune teller!```")
        await ctx.send("https://pm1.narvii.com/6151/eb4fe66bcc50f27617d4dce5c07fb3e9f7ab71a6_hq.jpg")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Psychic 'or Type like '%Psychic' or Type like 'Psychic%'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke.strip("(").strip(")").strip("'").strip("'").strip(",")
        gpoke=gpoke[:-1]
        gpoke=gpoke[1:]
        gpoke=gpoke[1:]
        gpoke=gpoke[:-1]
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Pokemon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
                await ctx.send("```It disappeared!```")
    @commands.command(name='darkforest',alias='dk')
    @charge(amount=100)
    async def darkforest(self, ctx):
        await ctx.send("```Let's go to the dark forest!```")
        await ctx.send("https://i.pinimg.com/originals/2e/65/a1/2e65a1c43b1de27adcbac1416df5a424.png")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Dark 'or Type like '%Dark' or Type like 'Dark%' or Type= 'Fire' or Type like 'Fire%' or Type like '%Fire'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke[:-1]
        gpoke=gpoke[1:]
        gpoke=gpoke[1:]
        gpoke=gpoke[:-1]
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Pokemon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
            await ctx.send("```It went to  Hide!```")
    @commands.command(name='meadow',alias='md')
    @charge(amount=100)
    async def meadow(self, ctx):
        await ctx.send("```Let's go to the meadow!```")
        await ctx.send("https://pre00.deviantart.net/e749/th/pre/i/2018/234/1/4/pokemon_meadow_by_shadow91smith-dckwwh3.png")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Grass 'or Type like '%Grass' or Type like 'Grass%' or Type= 'Bug' or Type like 'Bug%' or Type like '%Bug'or Type= 'Fairy' or Type like 'Fairy%' or Type like '%Fairy'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/pokes/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke[:-1]
        gpoke=gpoke[1:]
        gpoke=gpoke[1:]
        gpoke=gpoke[:-1]
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/wp-content/uploads/2019/03/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Pokemon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
                await ctx.send("```It went to frolick!```")



    @commands.command(name='fly',alias='fy')
    @charge(amount=100)
    async def fly(self, ctx):
        await ctx.send("```Let's soar!```")
        await ctx.send("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4YRkL_R_h7P2u1BsTwgkrJpkoMIheza8vZM5W8CH53xwKy4Rr")
        conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
        c = conn.cursor()
        c.execute("SELECT number FROM poke WHERE Type = 'Flying 'or Type like '%Flying' or Type like 'Flying%'")
        gpokes=c.fetchall()
        gspawn= rand.choice(gpokes)
        Ground=str(gspawn)
        Ground=Ground.strip("(").strip(")").strip(",")
        chosen_image ="http://pokepla.net/wp-content/uploads/photo-gallery/imported_from_media_libray/"+str(Ground)+".png"
        c.execute(f"SELECT Name FROM poke WHERE number='{Ground}'")
        gndpokename=c.fetchone()

        gpoke=str(gndpokename)
        gpoke=gpoke[:-1]
        gpoke=gpoke[1:]
        gpoke=gpoke[1:]
        gpoke=gpoke[:-1]
        gpoke=gpoke[:-1]
        if 'alo' in gpoke:
            Ground=Ground+'_61'
        else:
            print('not alolan')
        chosen_image ="http://pokepla.net/pokes/"+Ground+".png"
        await ctx.send(chosen_image)
        await ctx.send("```Oh! A Pokemon appeared!  Say the Pokemon's name to  catch it!```")
        miningcatch = await self.bot.wait_for("message",timeout=1900)
        if(miningcatch.content.casefold().capitalize() ==gpoke):
                self.count=0
                await ctx.send("```You caught the "+str(miningcatch.content)+"!```")
                conn = sqlite3.connect('/root/blazi/blaze/blazidb.db')
                c = conn.cursor()
                randlevel=rand.randint(1,70)
                randhp=rand.randint(0,31)
                randatk=rand.randint(0,31)
                randdef=rand.randint(0,31)
                randsp_atk=rand.randint(0,31)
                randsp_def=rand.randint(0,31)
                randsp=rand.randint(0,31)
                author=str(miningcatch.author.id)
                c.execute(f"SELECT numbercaught FROM OwnedPokes WHERE owner='{author}'")
                numberofpokes=c.fetchall()
                noofpokes=len(numberofpokes)
                newnumberofpokes=noofpokes+1
                c.close()
                c=conn.cursor()
                itemdrop='None'
                c.execute("INSERT into OwnedPokes(owner,id,numbercaught,item,level,hp,atk,def,spatk,spdef,speed,evs,form,exp,move1,move2,move3,move4) VALUES(?,?,?,?,?,?,?,?,?,?,?, 0, 'None' , 0 , 'Tackle' , 'Tackle' , 'Tackle' ,'Tackle')",(str(author),Ground,str(newnumberofpokes),str(itemdrop),str(randlevel),str(randhp),str(randatk),str(randdef),str(randsp_atk),str(randsp_def),str(randsp)))
                conn.commit()
                c.close()
        else:
                await ctx.send("```It went to  Land!```")
