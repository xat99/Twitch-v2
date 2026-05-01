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
from TwitchChannelPointsMiner.classes.Webhook import Webhook
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Matrix import Matrix
from TwitchChannelPointsMiner.classes.Pushover import Pushover
from TwitchChannelPointsMiner.classes.Gotify import Gotify
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

# Ezt a függvényt hívja meg az app.py az automatikus indításhoz
def start_miner():
    load_dotenv()

    # A bányász fő beállításai (Változatlanul)
    twitch_miner = TwitchChannelPointsMiner(
        username=os.getenv('TWITCH_USERNAME', ''),                  
        password=os.getenv('TWITCH_PASSWORD', ''),                  
        claim_drops_startup=False,                                  
        priority=[                                                  
            Priority.STREAK,                                        
            Priority.DROPS,                                         
            Priority.ORDER                                          
        ],
        enable_analytics=False,                                     
        disable_ssl_cert_verification=False,                        
        disable_at_in_nickname=False,                               
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
            make_predictions=True,
            follow_raid=True,
            claim_drops=True,
            claim_moments=True,
            watch_streak=True,
            community_goals=False,
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
                filter_condition=FilterCondition(
                    by=OutcomeKeys.TOTAL_USERS,
                    where=Condition.LTE,
                    value=800
                )
            )
        )
    )

    # A te saját csatornalistád (Változatlanul)
    streamers_list = [
        Streamer("ulrikch", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
        Streamer("nexuspwn", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
        Streamer("shadowmaci", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
        Streamer("komcsakogameplay", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
        Streamer("vravend", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
        Streamer("fyrexxx", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
        Streamer("picury", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),  
        Streamer("syluette", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),  
        Streamer("maeviis", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),  
        Streamer("nadia", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),      
        Streamer("bearguild", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),      
        Streamer("gabo01_", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),      
        Streamer("zsanyettka", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),      
        Streamer("fene__channel", settings=StreamerSettings(make_predictions=True  , follow_raid=True , claim_drops=True  , watch_streak=True , bet=BetSettings(strategy=Strategy.SMART      , percentage=5 , stealth_mode=True,  percentage_gap=20 , max_points=234   , filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS,      where=Condition.LTE, value=800 ) ) )),
    ]

    # MongoDB inicializálás (Változatlanul)
    mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
    client = MongoClient(mongo_url)
    db = client['twitch_miner_web']
    twitch_data_collection = db['twitch_data']

    for streamer in streamers_list:
        channel_name = streamer.username if isinstance(streamer, Streamer) else streamer
        if not twitch_data_collection.find_one({"channel_name": channel_name}):
            twitch_data_collection.insert_one({"channel_name": channel_name, "history": [0]})

    # Indul a bányászat! (Változatlanul)
    twitch_miner.mine(
        streamers_list,
        followers=False,
        followers_order=FollowersOrder.ASC
    )

if __name__ == '__main__':
    start_miner()
