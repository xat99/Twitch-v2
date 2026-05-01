# -*- coding: utf-8 -*-
import os
import logging
import threading
import time
import json
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
    
    # Alapadatok lekérése
    username = os.getenv('TWITCH_USERNAME', 'szaby')
    mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
    client = MongoClient(mongo_url)
    db = client['twitch_miner_web']
    twitch_data_collection = db['twitch_data']
    config_collection = db['config']

    # --- 2FA ÁTUGRÁS: SÜTI GENERÁLÁSA AZ ADATBÁZISBÓL ---
    saved_config = config_collection.find_one({"type": "twitch_tokens"})
    if saved_config and saved_config.get('auth_token'):
        cookie_data = [
            {"name": "auth-token", "value": saved_config.get('auth_token'), "domain": ".twitch.tv", "path": "/"},
            {"name": "unique_id", "value": saved_config.get('unique_id', ''), "domain": ".twitch.tv", "path": "/"}
        ]
        with open(f"{username}.json", "w") as f:
            json.dump(cookie_data, f)
        print(f"Log: Bejelentkezési fájl ({username}.json) létrehozva a weboldal adatai alapján.")

    # --- A BÁNYÁSZ FŐ BEÁLLÍTÁSAI (AZ ÖSSZES ÉRTESÍTŐVEL) ---
    twitch_miner = TwitchChannelPointsMiner(
        username=username,                  
        password=os.getenv('TWITCH_PASSWORD', ''),                  
        claim_drops_startup=False,                                  
        priority=[Priority.STREAK, Priority.DROPS, Priority.ORDER],
        enable_analytics=False,                                     
        logger_settings=LoggerSettings(
            save=True,                                              
            console_level=logging.INFO,                             
            console_username=False,                                 
            auto_clear=True,                                        
            time_zone="",                                           
            file_level=logging.DEBUG,                               
            emoji=True,                                             
            less=False,                                             
            colored=True,                                           
            color_palette=ColorPalette(                             
                STREAMER_online="GREEN",                            
                streamer_offline="red",                             
                BET_wiN=Fore.MAGENTA                                
            ),
            telegram=Telegram(
                chat_id=5856025580,
                token="7386173970:AAGAmPAXATMROzvEG5E2XLFmhryQhQBHO0g",
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                        Events.BET_LOSE, Events.CHAT_MENTION, Events.DROP_CLAIM, Events.DROP_STATUS],
                disable_notification=True,
            ),
            discord=Discord(
                webhook_api="https://discord.com/api/webhooks/1229673281963950131/-4kkB66hh0hm8tqxzUDhqTbfljlPZ2lNP1dNGox0QuJoXJoPFyF-8cYLxFFIDN1AhSW3",
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                        Events.BET_LOSE, Events.CHAT_MENTION, Events.DROP_CLAIM, Events.DROP_STATUS],
            ),
            webhook=Webhook(
                endpoint="https://example.com/webhook",
                method="GET",
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE, Events.CHAT_MENTION],
            ),
            matrix=Matrix(
                username="twitch_miner",
                password="...",
                homeserver="matrix.org",
                room_id="...",
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE],
            ),
            pushover=Pushover(
                userkey="YOUR-ACCOUNT-TOKEN",
                token="YOUR-APPLICATION-TOKEN",
                priority=0,
                sound="pushover",
                events=[Events.CHAT_MENTION, Events.DROP_CLAIM],
            ),
            gotify=Gotify(
                endpoint="https://example.com/message?token=TOKEN",
                priority=8,
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE, Events.CHAT_MENTION], 
            )
        ),
        streamer_settings=StreamerSettings(
            make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True,
            chat=ChatPresence.ONLINE,
            bet=BetSettings(
                strategy=Strategy.SMART, percentage=5, stealth_mode=True, delay_mode=DelayMode.FROM_END, delay=6,
                minimum_points=20000, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)
            )
        )
    )

    # --- CSATORNALISTA ---
    streamers_list = [
        Streamer("ulrikch", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("nexuspwn", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("shadowmaci", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("komcsakogameplay", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("vravend", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("fyrexxx", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("picury", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("syluette", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("maeviis", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("nadia", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("bearguild", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("gabo01_", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("zsanyettka", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("fene__channel", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800))))
    ]

    # --- ADATBÁZIS SZINKRONIZÁLÓ (A WEBOLDALNAK) ---
    def update_db_loop():
        time.sleep(60) # Várunk a bejelentkezésre
        while True:
            try:
                if hasattr(twitch_miner, 'streamers'):
                    for s_obj in twitch_miner.streamers:
                        twitch_data_collection.update_one(
                            {"channel_name": s_obj.username},
                            {"$push": {"history": {"$each": [int(s_obj.balance)], "$slice": -50}}},
                            upsert=True
                        )
                print("Log: Dashboard adatok frissítve.")
            except Exception as e:
                print(f"Log: Mentési hiba: {e}")
            time.sleep(120)

    threading.Thread(target=update_db_loop, daemon=True).start()

    # Indítás
    twitch_miner.mine(streamers_list, followers=False, followers_order=FollowersOrder.ASC)

if __name__ == '__main__':
    start_miner()
