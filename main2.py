import discord
import Globals
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def hello(ctx, sentence: discord.Option(str)):
    await ctx.respond(sentence)


@client.event
async def mj_imagine(ctx, prompt: discord.Option(str)):

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = PassPromptToSelfBot(prompt)

    if response.status_code >= 400:
        print(response.text)
        print(response.status_code)
        await ctx.respond("Request has failed; please try later")
    else:
        await ctx.respond(
            "Your image is being prepared, please wait a moment...")


@client.event
async def mj_upscale(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid argument, pick from 1 to 4")
        return

    if Globals.targetID == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    if (Globals.USE_MESSAGED_CHANNEL):
          Globals.CHANNEL_ID = ctx.channel.id
    response = Upscale(index, Globals.targetID, Globals.targetHash)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
        return

    await ctx.respond("Your image is being prepared, please wait a moment...")

@client.event
async def mj_upscale_to_max(ctx):
    if Globals.targetID == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = MaxUpscale(Globals.targetID, Globals.targetHash)
    Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
        return

    await ctx.respond("Your image is being prepared, please wait a moment...")

@client.event
async def mj_variation(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid argument, pick from 1 to 4")
        return

    if Globals.targetID == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return


    if (Globals.USE_MESSAGED_CHANNEL):
        Globals.CHANNEL_ID = ctx.channel.id

    response = Variation(index, Globals.targetID, Globals.targetHash)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
        return

    await ctx.respond("Your image is being prepared, please wait a moment...")



@client.event
async def on_message(message):
    if message.content == "": return
    if "$mj_target" in message.content and message.content[0] == '$':
        try:
            Globals.targetID = str(message.reference.message_id)
	    #Get the hash from the url
            Globals.targetHash = str((message.reference.resolved.attachments[0].url.split("_")[-1]).split(".")[0])
        except:
            await message.channel.send(
                "Exception has occured, maybe you didn't reply to MidJourney message"
            )
            await message.delete()
            return
        if str(message.reference.resolved.author.id) != Globals.MID_JOURNEY_ID:
            await message.channel.send(
                "Use the command only when you reply to MidJourney")
            await message.delete()
            return
        await message.channel.send("Done")
        await message.delete()


client.run(Globals.DAVINCI_TOKEN)