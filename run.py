# -*- coding: utf-8 -*-
import os
import logging
import threading
import time
import base64
import shutil
from colorama import Fore
from pymongo import MongoClient
from dotenv import load_dotenv

from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Webhook import Webhook
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Matrix import Matrix
from TwitchChannelPointsMiner.classes.Pushover import Pushover
from TwitchChannelPointsMiner.classes.Gotify import Gotify
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

def start_miner():
    load_dotenv()
    
    username = os.getenv('TWITCH_USERNAME', '0szaby0') 
    mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
    client = MongoClient(mongo_url)
    db = client['twitch_miner_web']
    twitch_data_collection = db['twitch_data']
    config_collection = db['config']

    session_file_root = f"{username}.pkl"
    session_file_cookies = os.path.join("cookies", f"{username}.pkl")

    if os.path.exists(session_file_root):
        os.makedirs("cookies", exist_ok=True)
        shutil.copy(session_file_root, session_file_cookies)

    saved_session = config_collection.find_one({"type": "session_file", "user": username})
    if saved_session:
        try:
            os.makedirs("cookies", exist_ok=True)
            with open(session_file_cookies, "wb") as f:
                f.write(base64.b64decode(saved_session['data']))
        except: pass

    twitch_miner = TwitchChannelPointsMiner(
        username=username,                  
        password=os.getenv('TWITCH_PASSWORD', ''),                  
        priority=[Priority.STREAK, Priority.DROPS, Priority.ORDER],
        logger_settings=LoggerSettings(
            save=True, console_level=logging.INFO, auto_clear=True, emoji=True, colored=True,
            color_palette=ColorPalette(STREAMER_online="GREEN", streamer_offline="red", BET_wiN=Fore.MAGENTA),
            telegram=Telegram(chat_id=5856025580, token="7386173970:AAGAmPAXATMROzvEG5E2XLFmhryQhQBHO0g", events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE, Events.CHAT_MENTION, Events.DROP_CLAIM, Events.DROP_STATUS]),
            discord=Discord(webhook_api="https://discord.com/api/webhooks/1229673281963950131/-4kkB66hh0hm8tqxzUDhqTbfljlPZ2lNP1dNGox0QuJoXJoPFyF-8cYLxFFIDN1AhSW3", events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE, Events.CHAT_MENTION, Events.DROP_CLAIM, Events.DROP_STATUS]),
            webhook=Webhook(endpoint="https://example.com/webhook", method="POST", events=[Events.STREAMER_ONLINE, Events.BET_LOSE]),
            matrix=Matrix(username="twitch_miner", password="...", homeserver="matrix.org", room_id="...", events=[Events.STREAMER_ONLINE]),
            pushover=Pushover(userkey="TOKEN", token="TOKEN", priority=0, sound="pushover", events=[Events.CHAT_MENTION]),
            gotify=Gotify(endpoint="https://example.com/gotify", priority=8, events=[Events.STREAMER_ONLINE]),
        ),
        streamer_settings=StreamerSettings(
            make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, chat=ChatPresence.ONLINE,
            bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, delay_mode=DelayMode.FROM_END, delay=6)
        )
    )

    streamers_list = [
        Streamer("ulrikch", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("nexuspwn", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("shadowmaci", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("komcsakogameplay", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("vravend", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("fyrexxx", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("picury", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("syluette", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("maeviis", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("nadia", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("bearguild", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("gabo01_", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("zsanyettka", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("fene__channel", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("lakatlindus", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800))))
    
    ]

    def sync_process():
        # Rövidebb indulási várakozás
        time.sleep(30) 
        while True:
            try:
                is_logged_in = False
                if hasattr(twitch_miner, 'streamers'):
                    for s in twitch_miner.streamers:
                        if not hasattr(s, 'channel_points') or s.channel_points is None: continue
                        
                        # --- LEKÉRJÜK AZ ÉLŐ STÁTUSZT ---
                        is_online = getattr(s, 'is_online', False)
                        
                        raw = str(s.channel_points).lower()
                        pts = int(float(raw.replace('k', '')) * 1000) if 'k' in raw else int(float(raw))
                        if pts > 0:
                            is_logged_in = True
                            twitch_data_collection.update_one(
                                {"channel_name": s.username}, 
                                {
                                    "$push": {"history": {"$each": [pts], "$slice": -50}},
                                    "$set": {"is_online": is_online} # Beírjuk a MongoDB-be, hogy Élő!
                                }, 
                                upsert=True
                            )
                
                if is_logged_in and os.path.exists(session_file_cookies):
                    if os.path.getsize(session_file_cookies) > 100:
                        with open(session_file_cookies, "rb") as f:
                            encoded_file = base64.b64encode(f.read()).decode('utf-8')
                            config_collection.update_one(
                                {"type": "session_file", "user": username},
                                {"$set": {"data": encoded_file, "last_sync": time.time()}},
                                upsert=True
                            )
            except Exception as e: pass
            
            # --- 3 PERC HELYETT MOST 1 PERCENKÉNT FRISSÍT ---
            time.sleep(60)

    threading.Thread(target=sync_process, daemon=True).start()
    twitch_miner.mine(streamers_list, followers=False, followers_order=FollowersOrder.ASC)

if __name__ == '__main__':
    start_miner()
