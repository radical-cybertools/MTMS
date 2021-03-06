import datetime

# results = {('localhost', 10, 4, 1, 0): [(datetime.timedelta(0, 24, 44567),
# datetime.timedelta(0, 0, 35434), datetime.timedelta(0, 13, 59402),
# datetime.timedelta(0, 10, 21073)), (datetime.timedelta(0, 22, 29079),
# datetime.timedelta(0, 0, 27898), datetime.timedelta(0, 11, 50547),
# datetime.timedelta(0, 10, 13244)), (datetime.timedelta(0, 28, 36546),
# datetime.timedelta(0, 0, 28613), datetime.timedelta(0, 17, 66181),
# datetime.timedelta(0, 10, 12988))], ('localhost', 10, 2, 1, 0):
# [(datetime.timedelta(0, 23, 39448), datetime.timedelta(0, 0, 36052),
# datetime.timedelta(0, 11, 719772), datetime.timedelta(0, 10, 19108)),
# (datetime.timedelta(0, 23, 43970), datetime.timedelta(0, 0, 37225),
# datetime.timedelta(0, 12, 54797), datetime.timedelta(0, 10, 20591)),
# (datetime.timedelta(0, 31, 52706), datetime.timedelta(0, 0, 34311),
# datetime.timedelta(0, 20, 81664), datetime.timedelta(0, 10, 19618))]}

# results = {('localhost', 10, 1, 4, 0): [(datetime.timedelta(0, 82, 148306),
# datetime.timedelta(0, 0, 134530), datetime.timedelta(0, 273, 252796),
# datetime.timedelta(0, 40, 93358)), (datetime.timedelta(0, 83, 188833),
# datetime.timedelta(0, 0, 147578), datetime.timedelta(0, 273, 499051),
# datetime.timedelta(0, 40, 120864)), (datetime.timedelta(0, 82, 251366),
# datetime.timedelta(0, 0, 144111), datetime.timedelta(0, 272, 663619),
# datetime.timedelta(0, 41, 133439))], ('localhost', 10, 1, 1, 0):
# [(datetime.timedelta(0, 22, 48258), datetime.timedelta(0, 0, 37604),
# datetime.timedelta(0, 11, 62349), datetime.timedelta(0, 10, 18680)),
# (datetime.timedelta(0, 22, 47534), datetime.timedelta(0, 0, 37611),
# datetime.timedelta(0, 11, 62394), datetime.timedelta(0, 10, 23739)),
# (datetime.timedelta(0, 22, 68265), datetime.timedelta(0, 0, 37695),
# datetime.timedelta(0, 11, 96978), datetime.timedelta(0, 10, 35099))],
# ('localhost', 10, 1, 2, 0): [(datetime.timedelta(0, 42, 84960),
# datetime.timedelta(0, 0, 72939), datetime.timedelta(0, 60, 262826),
# datetime.timedelta(0, 20, 41239)), (datetime.timedelta(0, 42, 99881),
# datetime.timedelta(0, 0, 85024), datetime.timedelta(0, 60, 264021),
# datetime.timedelta(0, 20, 47266)), (datetime.timedelta(0, 42, 126527),
# datetime.timedelta(0, 0, 74819), datetime.timedelta(0, 60, 350107),
# datetime.timedelta(0, 20, 59976))], ('localhost', 10, 1, 16, 0):
# [(datetime.timedelta(0, 325, 85400), datetime.timedelta(0, 0, 569685),
# datetime.timedelta(0, 4770, 654509), datetime.timedelta(0, 160, 836335)),
# (datetime.timedelta(0, 325, 340836), datetime.timedelta(0, 0, 562683),
# datetime.timedelta(0), datetime.timedelta(0)), (datetime.timedelta(0, 324,
# 277406), datetime.timedelta(0, 0, 548251), datetime.timedelta(0, 4772, 615903),
# datetime.timedelta(0, 160, 896145))], ('localhost', 10, 1, 8, 0):
# [(datetime.timedelta(0, 163, 359238), datetime.timedelta(0, 0, 237896),
# datetime.timedelta(0, 1157, 752494), datetime.timedelta(0, 80, 247204)),
# (datetime.timedelta(0, 163, 540142), datetime.timedelta(0, 0, 294106),
# datetime.timedelta(0, 1159, 573300), datetime.timedelta(0, 80, 336020)),
# (datetime.timedelta(0, 163, 531368), datetime.timedelta(0, 0, 285739),
# datetime.timedelta(0, 1159, 939769), datetime.timedelta(0, 80, 352921))],
# ('localhost', 10, 4, 4, 0): [(datetime.timedelta(0, 22, 70545),
# datetime.timedelta(0, 0, 137722), datetime.timedelta(0, 44, 515873),
# datetime.timedelta(0, 40, 377912)), (datetime.timedelta(0, 23, 73221),
# datetime.timedelta(0, 0, 125783), datetime.timedelta(0, 44, 595462),
# datetime.timedelta(0, 40, 389014))], ('localhost', 10, 8, 16, 0):
# [(datetime.timedelta(0, 43, 211235), datetime.timedelta(0, 0, 456870),
# datetime.timedelta(0, 489, 288593), datetime.timedelta(0, 163, 129143))],
# ('localhost', 10, 2, 1, 0): [(datetime.timedelta(0, 24, 40121),
# datetime.timedelta(0, 0, 32330), datetime.timedelta(0, 12, 800976),
# datetime.timedelta(0, 10, 15214)), (datetime.timedelta(0, 24, 45568),
# datetime.timedelta(0, 0, 37183), datetime.timedelta(0, 13, 71856),
# datetime.timedelta(0, 10, 15984))], ('localhost', 10, 4, 8, 0):
# [(datetime.timedelta(0, 43, 122340), datetime.timedelta(0, 0, 256403),
# datetime.timedelta(0, 246, 972602), datetime.timedelta(0, 84, 821866))],
# ('localhost', 10, 8, 4, 0): [(datetime.timedelta(0, 22, 50923),
# datetime.timedelta(0, 0, 117490), datetime.timedelta(0, 44, 428544),
# datetime.timedelta(0, 40, 369352))], ('localhost', 10, 8, 8, 0):
# [(datetime.timedelta(0, 24, 78150), datetime.timedelta(0, 0, 225897),
# datetime.timedelta(0, 105, 738459), datetime.timedelta(0, 81, 429706))],
# ('localhost', 10, 4, 16, 0): [(datetime.timedelta(0, 83, 333606),
# datetime.timedelta(0, 0, 502420), datetime.timedelta(0, 1106, 459458),
# datetime.timedelta(0, 162, 11351))], ('localhost', 10, 2, 8, 0):
# [(datetime.timedelta(0, 82, 204735), datetime.timedelta(0, 0, 257420),
# datetime.timedelta(0, 548, 326704), datetime.timedelta(0, 80, 459323)),
# (datetime.timedelta(0, 83, 222844), datetime.timedelta(0, 0, 275600),
# datetime.timedelta(0, 548, 492650), datetime.timedelta(0, 80, 462054))],
# ('localhost', 10, 2, 2, 0): [(datetime.timedelta(0, 23, 52378),
# datetime.timedelta(0, 0, 66631), datetime.timedelta(0, 24, 134737),
# datetime.timedelta(0, 20, 90353)), (datetime.timedelta(0, 22, 40751),
# datetime.timedelta(0, 0, 60784), datetime.timedelta(0, 22, 196476),
# datetime.timedelta(0, 20, 81682))], ('localhost', 10, 2, 4, 0):
# [(datetime.timedelta(0, 43, 109030), datetime.timedelta(0, 0, 130940),
# datetime.timedelta(0, 120, 792436), datetime.timedelta(0, 40, 178314)),
# (datetime.timedelta(0, 42, 105453), datetime.timedelta(0, 0, 137652),
# datetime.timedelta(0, 120, 986955), datetime.timedelta(0, 40, 199532))],
# ('localhost', 10, 8, 1, 0): [(datetime.timedelta(0, 23, 40264),
# datetime.timedelta(0, 0, 34563), datetime.timedelta(0, 12, 69626),
# datetime.timedelta(0, 10, 20425))], ('localhost', 10, 8, 2, 0):
# [(datetime.timedelta(0, 22, 48479), datetime.timedelta(0, 0, 68241),
# datetime.timedelta(0, 22, 157034), datetime.timedelta(0, 20, 83844))],
# ('localhost', 10, 2, 16, 0): [(datetime.timedelta(0, 163, 560431),
# datetime.timedelta(0, 0, 514815), datetime.timedelta(0, 2324, 395058),
# datetime.timedelta(0, 161, 125035)), (datetime.timedelta(0, 163, 542845),
# datetime.timedelta(0, 0, 509019), datetime.timedelta(0, 2325, 688947),
# datetime.timedelta(0, 161, 161442))], ('localhost', 10, 4, 1, 0):
# [(datetime.timedelta(0, 25, 48046), datetime.timedelta(0, 0, 35631),
# datetime.timedelta(0, 14, 70044), datetime.timedelta(0, 10, 19413)),
# (datetime.timedelta(0, 23, 48006), datetime.timedelta(0, 0, 36852),
# datetime.timedelta(0, 12, 94994), datetime.timedelta(0, 10, 21291))],
# ('localhost', 10, 4, 2, 0): [(datetime.timedelta(0, 23, 50560),
# datetime.timedelta(0, 0, 67295), datetime.timedelta(0, 24, 183888),
# datetime.timedelta(0, 20, 89524)), (datetime.timedelta(0, 24, 52398),
# datetime.timedelta(0, 0, 66694), datetime.timedelta(0, 24, 206788),
# datetime.timedelta(0, 20, 89221))]}

# {('localhost', 8, 1, 16, 0): [(datetime.timedelta(0, 259, 734656),
# datetime.timedelta(0, 0, 416375), datetime.timedelta(0, 3768, 450433),
# datetime.timedelta(0, 128, 602123))], ('localhost', 8, 8, 16, 0):
# [(datetime.timedelta(0, 35, 188781), datetime.timedelta(0, 0, 379610),
# datetime.timedelta(0, 393, 234594), datetime.timedelta(0, 130, 597508))],
# ('localhost', 8, 1, 4, 0): [(datetime.timedelta(0, 67, 98928),
# datetime.timedelta(0, 0, 107573), datetime.timedelta(0, 217, 80865),
# datetime.timedelta(0, 32, 79901)), (datetime.timedelta(0, 66, 175674),
# datetime.timedelta(0, 0, 110242), datetime.timedelta(0, 216, 140620),
# datetime.timedelta(0, 33, 100874))], ('localhost', 8, 8, 4, 0):
# [(datetime.timedelta(0, 19, 69305), datetime.timedelta(0, 0, 101653),
# datetime.timedelta(0, 36, 534113), datetime.timedelta(0, 32, 330647))],
# ('localhost', 8, 2, 8, 0): [(datetime.timedelta(0, 66, 213899),
# datetime.timedelta(0, 0, 200261), datetime.timedelta(0, 435, 471080),
# datetime.timedelta(0, 64, 346809))], ('localhost', 8, 4, 2, 0):
# [(datetime.timedelta(0, 19, 43440), datetime.timedelta(0, 0, 49313),
# datetime.timedelta(0, 20, 132882), datetime.timedelta(0, 16, 67510))],
# ('localhost', 8, 8, 2, 0): [(datetime.timedelta(0, 19, 64696),
# datetime.timedelta(0, 0, 54610), datetime.timedelta(0, 20, 173738),
# datetime.timedelta(0, 16, 89085))], ('localhost', 8, 4, 8, 0):
# [(datetime.timedelta(0, 36, 152576), datetime.timedelta(0, 0, 221854),
# datetime.timedelta(0, 206, 529010), datetime.timedelta(0, 68, 711077))],
# ('localhost', 8, 2, 16, 0): [(datetime.timedelta(0, 131, 529835),
# datetime.timedelta(0, 0, 401323), datetime.timedelta(0, 1842, 162300),
# datetime.timedelta(0, 128, 974294))], ('localhost', 8, 4, 4, 0):
# [(datetime.timedelta(0, 18, 61689), datetime.timedelta(0, 0, 98431),
# datetime.timedelta(0, 36, 519979), datetime.timedelta(0, 32, 296752))],
# ('localhost', 8, 8, 1, 0): [(datetime.timedelta(0, 19, 60299),
# datetime.timedelta(0, 0, 31837), datetime.timedelta(0, 10, 69199),
# datetime.timedelta(0, 8, 23749))], ('localhost', 8, 2, 4, 0):
# [(datetime.timedelta(0, 34, 145691), datetime.timedelta(0, 0, 129194),
# datetime.timedelta(0, 96, 741682), datetime.timedelta(0, 32, 195947))],
# ('localhost', 8, 8, 8, 0): [(datetime.timedelta(0, 18, 108809),
# datetime.timedelta(0, 0, 204507), datetime.timedelta(0, 73, 274821),
# datetime.timedelta(0, 65, 239296))], ('localhost', 8, 1, 1, 0):
# [(datetime.timedelta(0, 18, 28268), datetime.timedelta(0, 0, 26209),
# datetime.timedelta(0, 9, 75020), datetime.timedelta(0, 8, 8411)),
# (datetime.timedelta(0, 21, 51024), datetime.timedelta(0, 0, 29923),
# datetime.timedelta(0, 11, 64547), datetime.timedelta(0, 8, 22204))],
# ('localhost', 8, 4, 16, 0): [(datetime.timedelta(0, 67, 351454),
# datetime.timedelta(0, 0, 429593), datetime.timedelta(0, 875, 802048),
# datetime.timedelta(0, 129, 566243))], ('localhost', 8, 1, 8, 0):
# [(datetime.timedelta(0, 130, 321702), datetime.timedelta(0, 0, 203967),
# datetime.timedelta(0, 916, 476239), datetime.timedelta(0, 64, 187441))],
# ('localhost', 8, 4, 1, 0): [(datetime.timedelta(0, 20, 53993),
# datetime.timedelta(0, 0, 28493), datetime.timedelta(0, 11, 83037),
# datetime.timedelta(0, 8, 21723))], ('localhost', 8, 1, 2, 0):
# [(datetime.timedelta(0, 34, 71836), datetime.timedelta(0, 0, 53276),
# datetime.timedelta(0, 48, 237322), datetime.timedelta(0, 16, 36103)),
# (datetime.timedelta(0, 35, 91398), datetime.timedelta(0, 0, 57060),
# datetime.timedelta(0, 49, 308996), datetime.timedelta(0, 17, 51915))],
# ('localhost', 8, 2, 1, 0): [(datetime.timedelta(0, 25, 66243),
# datetime.timedelta(0, 0, 29679), datetime.timedelta(0, 16, 77152),
# datetime.timedelta(0, 8, 20110))], ('localhost', 8, 2, 2, 0):
# [(datetime.timedelta(0, 19, 57072), datetime.timedelta(0, 0, 55590),
# datetime.timedelta(0, 20, 166452), datetime.timedelta(0, 16, 82779))]}


results = {('localhost', 8, 1, 16, 0): [(datetime.timedelta(0, 259, 837489),
datetime.timedelta(0, 0, 466942), datetime.timedelta(0, 3769, 765585),
datetime.timedelta(0, 128, 630636)), (datetime.timedelta(0, 260, 792232),
datetime.timedelta(0, 0, 445014), datetime.timedelta(0),
datetime.timedelta(0)), (datetime.timedelta(0, 259, 753113),
datetime.timedelta(0, 0, 431306), datetime.timedelta(0, 3769, 40693),
datetime.timedelta(0, 128, 579386))], ('localhost', 8, 8, 16, 0):
[(datetime.timedelta(0, 35, 157145), datetime.timedelta(0, 0, 371099),
datetime.timedelta(0, 392, 957538), datetime.timedelta(0, 130, 466413)),
(datetime.timedelta(0, 35, 199505), datetime.timedelta(0, 0, 375314),
datetime.timedelta(0, 401, 526427), datetime.timedelta(0, 136, 395596)),
(datetime.timedelta(0, 35, 162089), datetime.timedelta(0, 0, 381369),
datetime.timedelta(0, 392, 829193), datetime.timedelta(0, 130, 575435))],
('localhost', 8, 1, 4, 0): [(datetime.timedelta(0, 67, 152389),
datetime.timedelta(0, 0, 109691), datetime.timedelta(0, 217, 93864),
datetime.timedelta(0, 32, 83365)), (datetime.timedelta(0, 66, 155029),
datetime.timedelta(0, 0, 117289), datetime.timedelta(0, 217, 128742),
datetime.timedelta(0, 32, 83109)), (datetime.timedelta(0, 66, 156255),
datetime.timedelta(0, 0, 110726), datetime.timedelta(0, 217, 295642),
datetime.timedelta(0, 32, 82244))], ('localhost', 8, 8, 4, 0):
[(datetime.timedelta(0, 18, 65955), datetime.timedelta(0, 0, 115312),
datetime.timedelta(0, 36, 431068), datetime.timedelta(0, 32, 298970)),
(datetime.timedelta(0, 18, 60873), datetime.timedelta(0, 0, 109302),
datetime.timedelta(0, 36, 615296), datetime.timedelta(0, 32, 301629)),
(datetime.timedelta(0, 19, 60575), datetime.timedelta(0, 0, 106844),
datetime.timedelta(0, 39, 704008), datetime.timedelta(0, 32, 327365))],
('localhost', 8, 2, 8, 0): [(datetime.timedelta(0, 66, 231533),
datetime.timedelta(0, 0, 230796), datetime.timedelta(0, 435, 591504),
datetime.timedelta(0, 64, 402460)), (datetime.timedelta(0, 67, 184119),
datetime.timedelta(0, 0, 216973), datetime.timedelta(0, 435, 394175),
datetime.timedelta(0, 64, 345780)), (datetime.timedelta(0, 66, 205364),
datetime.timedelta(0, 0, 246392), datetime.timedelta(0, 435, 237038),
datetime.timedelta(0, 66, 405120))], ('localhost', 8, 4, 2, 0):
[(datetime.timedelta(0, 18, 62100), datetime.timedelta(0, 0, 63961),
datetime.timedelta(0, 18, 174140), datetime.timedelta(0, 16, 87890)),
(datetime.timedelta(0, 18, 44803), datetime.timedelta(0, 0, 56146),
datetime.timedelta(0, 18, 215687), datetime.timedelta(0, 16, 69692)),
(datetime.timedelta(0, 18, 60701), datetime.timedelta(0, 0, 59090),
datetime.timedelta(0, 18, 264181), datetime.timedelta(0, 16, 90927))],
('localhost', 8, 8, 2, 0): [(datetime.timedelta(0, 22, 70144),
datetime.timedelta(0, 0, 58994), datetime.timedelta(0, 24, 220092),
datetime.timedelta(0, 18, 87336)), (datetime.timedelta(0, 18, 50610),
datetime.timedelta(0, 0, 59899), datetime.timedelta(0, 18, 244575),
datetime.timedelta(0, 16, 78805)), (datetime.timedelta(0, 18, 44198),
datetime.timedelta(0, 0, 55247), datetime.timedelta(0, 18, 214092),
datetime.timedelta(0, 16, 71950))], ('localhost', 8, 4, 8, 0):
[(datetime.timedelta(0, 34, 145306), datetime.timedelta(0, 0, 205697),
datetime.timedelta(0, 194, 569979), datetime.timedelta(0, 64, 712417)),
(datetime.timedelta(0, 34, 98885), datetime.timedelta(0, 0, 194877),
datetime.timedelta(0, 194, 663869), datetime.timedelta(0, 64, 649599)),
(datetime.timedelta(0, 35, 152753), datetime.timedelta(0, 0, 214815),
datetime.timedelta(0, 194, 905600), datetime.timedelta(0, 64, 717372))],
('localhost', 8, 2, 16, 0): [(datetime.timedelta(0, 131, 534165),
datetime.timedelta(0, 0, 433852), datetime.timedelta(0, 1842, 804461),
datetime.timedelta(0, 129, 34434)), (datetime.timedelta(0, 131, 434763),
datetime.timedelta(0, 0, 425663), datetime.timedelta(0, 1839, 634390),
datetime.timedelta(0, 129, 38721)), (datetime.timedelta(0, 131, 485394),
datetime.timedelta(0, 0, 419457), datetime.timedelta(0, 1842, 382251),
datetime.timedelta(0, 128, 979864))], ('localhost', 8, 4, 4, 0):
[(datetime.timedelta(0, 18, 73930), datetime.timedelta(0, 0, 111473),
datetime.timedelta(0, 36, 440192), datetime.timedelta(0, 32, 335847)),
(datetime.timedelta(0, 18, 55432), datetime.timedelta(0, 0, 107844),
datetime.timedelta(0, 36, 593519), datetime.timedelta(0, 32, 297006)),
(datetime.timedelta(0, 18, 72842), datetime.timedelta(0, 0, 107662),
datetime.timedelta(0, 36, 754673), datetime.timedelta(0, 32, 329478))],
('localhost', 8, 8, 1, 0): [(datetime.timedelta(0, 18, 52219),
datetime.timedelta(0, 0, 31568), datetime.timedelta(0, 9, 54845),
datetime.timedelta(0, 8, 24616)), (datetime.timedelta(0, 21, 42570),
datetime.timedelta(0, 0, 29839), datetime.timedelta(0, 11, 102569),
datetime.timedelta(0, 8, 16050)), (datetime.timedelta(0, 20, 38713),
datetime.timedelta(0, 0, 28389), datetime.timedelta(0, 11, 119163),
datetime.timedelta(0, 8, 13747))], ('localhost', 8, 2, 4, 0):
[(datetime.timedelta(0, 34, 93329), datetime.timedelta(0, 0, 107738),
datetime.timedelta(0, 96, 714166), datetime.timedelta(0, 32, 160623)),
(datetime.timedelta(0, 35, 87472), datetime.timedelta(0, 0, 109986),
datetime.timedelta(0, 98, 786971), datetime.timedelta(0, 34, 158313)),
(datetime.timedelta(0, 35, 100639), datetime.timedelta(0, 0, 119274),
datetime.timedelta(0, 96, 913952), datetime.timedelta(0, 32, 165282))],
('localhost', 8, 8, 8, 0): [(datetime.timedelta(0, 19, 86859),
datetime.timedelta(0, 0, 181376), datetime.timedelta(0, 73, 332112),
datetime.timedelta(0, 65, 112436)), (datetime.timedelta(0, 25, 81319),
datetime.timedelta(0, 0, 181529), datetime.timedelta(0, 121, 837642),
datetime.timedelta(0, 69, 960707)), (datetime.timedelta(0, 22, 82599),
datetime.timedelta(0, 0, 180330), datetime.timedelta(0, 97, 971086),
datetime.timedelta(0, 73, 167327))], ('localhost', 8, 1, 1, 0):
[(datetime.timedelta(0, 19, 35608), datetime.timedelta(0, 0, 31999),
datetime.timedelta(0, 10, 84171), datetime.timedelta(0, 8, 15169)),
(datetime.timedelta(0, 19, 38439), datetime.timedelta(0, 0, 30356),
datetime.timedelta(0, 10, 82767), datetime.timedelta(0, 8, 14566)),
(datetime.timedelta(0, 21, 42968), datetime.timedelta(0, 0, 28790),
datetime.timedelta(0, 12, 103688), datetime.timedelta(0, 8, 18980))],
('localhost', 8, 4, 16, 0): [(datetime.timedelta(0, 67, 310084),
datetime.timedelta(0, 0, 398889), datetime.timedelta(0, 887, 641083),
datetime.timedelta(0, 129, 529041)), (datetime.timedelta(0, 67, 236154),
datetime.timedelta(0, 0, 399956), datetime.timedelta(0, 871, 780613),
datetime.timedelta(0, 133, 473217)), (datetime.timedelta(0, 67, 254692),
datetime.timedelta(0, 0, 382555), datetime.timedelta(0, 877, 692464),
datetime.timedelta(0, 130, 484))], ('localhost', 8, 1, 8, 0):
[(datetime.timedelta(0, 130, 327306), datetime.timedelta(0, 0, 241794),
datetime.timedelta(0, 917, 196067), datetime.timedelta(0, 64, 207514)),
(datetime.timedelta(0, 131, 303804), datetime.timedelta(0, 0, 211089),
datetime.timedelta(0, 924, 179422), datetime.timedelta(0, 65, 205385)),
(datetime.timedelta(0, 131, 319105), datetime.timedelta(0, 0, 213023),
datetime.timedelta(0, 918, 83003), datetime.timedelta(0, 64, 192096))],
('localhost', 8, 4, 1, 0): [(datetime.timedelta(0, 25, 72521),
datetime.timedelta(0, 0, 30121), datetime.timedelta(0, 16, 59761),
datetime.timedelta(0, 8, 23739)), (datetime.timedelta(0, 19, 36145),
datetime.timedelta(0, 0, 27986), datetime.timedelta(0, 10, 105769),
datetime.timedelta(0, 8, 12870)), (datetime.timedelta(0, 18, 56242),
datetime.timedelta(0, 0, 30709), datetime.timedelta(0, 9, 114291),
datetime.timedelta(0, 8, 27432))], ('localhost', 8, 1, 2, 0):
[(datetime.timedelta(0, 34, 72993), datetime.timedelta(0, 0, 53220),
datetime.timedelta(0, 48, 198982), datetime.timedelta(0, 16, 39300)),
(datetime.timedelta(0, 34, 72177), datetime.timedelta(0, 0, 54790),
datetime.timedelta(0, 48, 325029), datetime.timedelta(0, 16, 35081)),
(datetime.timedelta(0, 35, 74838), datetime.timedelta(0, 0, 58854),
datetime.timedelta(0, 48, 321656), datetime.timedelta(0, 16, 33337))],
('localhost', 8, 2, 1, 0): [(datetime.timedelta(0, 19, 39166),
datetime.timedelta(0, 0, 30492), datetime.timedelta(0, 10, 50076),
datetime.timedelta(0, 8, 16452)), (datetime.timedelta(0, 23, 45086),
datetime.timedelta(0, 0, 30399), datetime.timedelta(0, 14, 78725),
datetime.timedelta(0, 8, 15202)), (datetime.timedelta(0, 22, 41577),
datetime.timedelta(0, 0, 29445), datetime.timedelta(0, 13, 117125),
datetime.timedelta(0, 8, 17334))], ('localhost', 8, 2, 2, 0):
[(datetime.timedelta(0, 19, 41444), datetime.timedelta(0, 0, 55664),
datetime.timedelta(0, 20, 175112), datetime.timedelta(0, 16, 77672)),
(datetime.timedelta(0, 19, 47632), datetime.timedelta(0, 0, 55231),
datetime.timedelta(0, 18, 219468), datetime.timedelta(0, 16, 72579)),
(datetime.timedelta(0, 18, 46335), datetime.timedelta(0, 0, 54458),
datetime.timedelta(0, 18, 255839), datetime.timedelta(0, 16, 75394))]}
