# -*- coding: utf-8 -*-

import os
import logging
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

    mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
    client = MongoClient(mongo_url)
    db = client['twitch_miner_web']
    twitch_data_collection = db['twitch_data']

    # KIVETTEM a handle_signals=False-t, mert hibát dobott
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

    for streamer in streamers_list:
        name = streamer.username if hasattr(streamer, 'username') else streamer
        if not twitch_data_collection.find_one({"channel_name": name}):
            twitch_data_collection.insert_one({"channel_name": name, "history": [0]})

    twitch_miner.mine(streamers_list, followers=False, followers_order=FollowersOrder.ASC)
