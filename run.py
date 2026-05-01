# -*- coding: utf-8 -*-

import os
import logging
import threading
import time
from colorama import Fore
from pymongo import MongoClient
from dotenv import load_dotenv

from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

def start_miner():
    load_dotenv()

    # MongoDB kapcsolat - Renderen a MONGO_URI változóba az Atlas linked kell!
    mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
    client = MongoClient(mongo_url)
    db = client['twitch_miner_web']
    twitch_data_collection = db['twitch_data']

    twitch_miner = TwitchChannelPointsMiner(
        username=os.getenv('TWITCH_USERNAME', ''),                  
        password=os.getenv('TWITCH_PASSWORD', ''),                  
        claim_drops_startup=False,                                  
        priority=[Priority.STREAK, Priority.DROPS, Priority.ORDER],
        enable_analytics=False,                                     
        logger_settings=LoggerSettings(
            save=True,                                              
            console_level=logging.INFO,                             
            auto_clear=True,
            emoji=True,
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
        ),
        streamer_settings=StreamerSettings(
            make_predictions=True,
            follow_raid=True,
            claim_drops=True,
            watch_streak=True,
            chat=ChatPresence.ONLINE,
            bet=BetSettings(
                strategy=Strategy.SMART,
                percentage=5,
                percentage_gap=20,
                max_points=50000,
                stealth_mode=True,
                delay_mode=DelayMode.FROM_END,
                delay=6,
                minimum_points=20000,
                filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)
            )
        )
    )

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

    # Kezdeti szinkronizálás: biztosítjuk, hogy minden csatorna benne legyen az adatbázisban
    for streamer in streamers_list:
        name = streamer.username if hasattr(streamer, 'username') else streamer
        if not twitch_data_collection.find_one({"channel_name": name}):
            twitch_data_collection.insert_one({"channel_name": name, "history": [0]})

    # --- OKOSABB ADATMENTŐ FÜGGVÉNY ---
    def update_db_loop():
        print("Log: Adatmentő szál várakozik 60 másodpercet a bejelentkezésig...")
        time.sleep(60) 
        while True:
            try:
                print("Log: Pontszámok mentése folyamatban...")
                for streamer in streamers_list:
                    name = streamer.username if hasattr(streamer, 'username') else streamer
                    points = None
                    
                    # Megpróbáljuk kinyerni a pontokat a bot belső állapotából
                    try:
                        if hasattr(twitch_miner, 'get_points'):
                            points = twitch_miner.get_points(name)
                        
                        # Ha az első nem megy, megpróbáljuk a belső listát (sok forknál ez kell)
                        if points is None and hasattr(twitch_miner, 'streamers'):
                            s_obj = next((s for s in twitch_miner.streamers if s.username == name), None)
                            if s_obj:
                                points = s_obj.balance
                    except Exception as e:
                        print(f"Log: Hiba {name} pontjainak lekérésekor: {e}")

                    # Csak akkor mentünk, ha kaptunk számot és az nem nulla (vagy változott)
                    if points is not None:
                        twitch_data_collection.update_one(
                            {"channel_name": name},
                            {"$push": {"history": {"$each": [int(points)], "$slice": -50}}}
                        )
                print("Log: Adatok sikeresen frissítve az adatbázisban.")
            except Exception as e:
                print(f"Log: Váratlan hiba az adatmentő körben: {e}")
            time.sleep(300) # 5 percenként ismételjük

    # Adatmentő indítása a háttérben
    db_thread = threading.Thread(target=update_db_loop, daemon=True)
    db_thread.start()

    # Indul a bányászat a fő szálon
    twitch_miner.mine(streamers_list, followers=False, followers_order=FollowersOrder.ASC)

if __name__ == '__main__':
    start_miner()
