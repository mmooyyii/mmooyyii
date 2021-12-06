import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


"""
2 013
2 031
2 301
"""


def make_available():
    ans = {}
    for k in range(0b0000, 0b1111 + 1):
        b = bin(k)[2:].zfill(4)
        tmp = []
        if b[1] == '0' and k != 0:  # 0前不能有1,最高位数字不为0
            tmp.append(0)
        if b[0] == '1':  # 1前一定有0
            tmp.append(1)
        if b[3] == '0':
            tmp.append(2)
        if b[2] == '1':
            tmp.append(3)
        ans[k] = tmp
    return ans


available = make_available()

from functools import lru_cache

mod = int(1e9) + 7


@lru_cache(None)
def dp(n, status, pre):
    if n == 0:
        return 1 if status == 0b1111 else 0
    ava = available[status]
    ans = 0
    for i in ava:
        if i != pre:
            for use in range(1, n + 1):
                ans += dp(n - use, status | (1 << (3 - i)), i)
    return ans % mod


def force(n):
    ans = 0
    import re
    l, r = 10 ** (n - 1), 10 ** n
    print(l, r)
    for i in range(l, r):
        i = str(i)
        if set("0123") == set(i):
            if re.findall("3.*?2", i) or re.findall("1.*?0", i):
                pass
            else:
                ans += 1
    return ans


def make_table():
    ans = {}
    for i in range(4, 1001):
        ans[i] = dp(i, 0b0000, None)
    print(ans)


ans = {4: 3, 5: 20, 6: 85, 7: 294, 8: 903, 9: 2568, 10: 6921, 11: 17930, 12: 45067, 13: 110604, 14: 266253, 15: 630798,
       16: 1474575, 17: 3407888, 18: 7798801, 19: 17694738, 20: 39845907, 21: 89128980, 22: 198180885, 23: 438304790,
       24: 964689943, 25: 113929226, 26: 613734397, 27: 32775124, 28: 743271816, 29: 976204506, 30: 200166234,
       31: 432717871, 32: 3948385, 33: 432405732, 34: 8796671, 35: 895498336, 36: 726675735, 37: 684447765,
       38: 550564413, 39: 903419146, 40: 289323979, 41: 299429427, 42: 552041912, 43: 33690130, 44: 973073250,
       45: 850493135, 46: 695600860, 47: 752273493, 48: 970375663, 49: 359778886, 50: 532353289, 51: 639778320,
       52: 328661495, 53: 553455410, 54: 495021005, 55: 957953036, 56: 235109359, 57: 875387761, 58: 94638425,
       59: 944052301, 60: 531754664, 61: 619007774, 62: 885409001, 63: 138397960, 64: 157541918, 65: 367747896,
       66: 423167974, 67: 386368383, 68: 182177717, 69: 841989443, 70: 956751020, 71: 94054497, 72: 819230256,
       73: 440735589, 74: 566086420, 75: 661533404, 76: 702048027, 77: 802578604, 78: 683162454, 79: 84415620,
       80: 729173045, 81: 827350332, 82: 889350365, 83: 241282483, 84: 394293118, 85: 585171712, 86: 709772641,
       87: 390920166, 88: 509622933, 89: 44876624, 90: 281145814, 91: 225338741, 92: 337295599, 93: 568875121,
       94: 168413372, 95: 882343512, 96: 824101438, 97: 703793405, 98: 392291172, 99: 501037584, 100: 929078566,
       101: 700349656, 102: 61455742, 103: 397167019, 104: 248330312, 105: 215623503, 106: 491113320, 107: 345840266,
       108: 906669700, 109: 218841431, 110: 199734260, 111: 825665849, 112: 307915289, 113: 537375569, 114: 134596589,
       115: 822394938, 116: 618214954, 117: 917323112, 118: 664518589, 119: 924953731, 120: 914084073, 121: 701208271,
       122: 637870483, 123: 725396100, 124: 307596841, 125: 243791606, 126: 574756204, 127: 983812546, 128: 956133555,
       129: 529100302, 130: 571499404, 131: 728861088, 132: 747975964, 133: 313517834, 134: 736284027, 135: 639297696,
       136: 508520416, 137: 269822223, 138: 631069783, 139: 616715190, 140: 286031409, 141: 364164311, 142: 686330322,
       143: 36261322, 144: 894918461, 145: 425017270, 146: 101172581, 147: 666175780, 148: 183121685, 149: 914001305,
       150: 615953651, 151: 192679624, 152: 76644220, 153: 75338873, 154: 73739436, 155: 151523752, 156: 626980115,
       157: 533510990, 158: 889494453, 159: 950675585, 160: 298207848, 161: 497095559, 162: 9483654, 163: 477417872,
       164: 727467657, 165: 711660566, 166: 359694336, 167: 437980327, 168: 4834269, 169: 650796237, 170: 350608598,
       171: 332770774, 172: 995691185, 173: 785766412, 174: 428470312, 175: 107154233, 176: 787412774, 177: 866388132,
       178: 606609225, 179: 542299793, 180: 905592927, 181: 778833651, 182: 144284965, 183: 764449232, 184: 85944780,
       185: 496557494, 186: 63601225, 187: 110475517, 188: 872098152, 189: 415692298, 190: 912779973, 191: 465157245,
       192: 163122028, 193: 699084812, 194: 958302274, 195: 665771950, 196: 87682733, 197: 203251000, 198: 493488578,
       199: 223381133, 200: 44431690, 201: 533924967, 202: 457418363, 203: 692863926, 204: 939562725, 205: 982355944,
       206: 162294173, 207: 701995338, 208: 123289233, 209: 614144573, 210: 821359094, 211: 544733362, 212: 325247437,
       213: 985556817, 214: 368238305, 215: 984727370, 216: 373958824, 217: 372930783, 218: 627897524, 219: 283886114,
       220: 151992468, 221: 528501404, 222: 618187484, 223: 583047598, 224: 308046795, 225: 797209255, 226: 751074520,
       227: 404310221, 228: 790640912, 229: 900718723, 230: 151102946, 231: 423120100, 232: 931234758, 233: 718790683,
       234: 522887603, 235: 961715251, 236: 245965470, 237: 118310444, 238: 451998766, 239: 259990775, 240: 82442798,
       241: 990757382, 242: 35156632, 243: 981393440, 244: 392539784, 245: 859770312, 246: 299291689, 247: 618824464,
       248: 999608729, 249: 966092076, 250: 751843191, 251: 914823822, 252: 195560975, 253: 210225296, 254: 233210363,
       255: 441046178, 256: 529554824, 257: 750457469, 258: 676456092, 259: 289685271, 260: 624298028, 261: 681213363,
       262: 913185769, 263: 298938212, 264: 285106719, 265: 428867629, 266: 543430576, 267: 395025400, 268: 279926266,
       269: 286697135, 270: 521270548, 271: 926667525, 272: 598335382, 273: 640166138, 274: 74312149, 275: 550562047,
       276: 532955280, 277: 185484059, 278: 121937106, 279: 769455882, 280: 637362191, 281: 566199171, 282: 904495508,
       283: 731480227, 284: 64528371, 285: 845371302, 286: 149728827, 287: 270144089, 288: 587088703, 289: 478633477,
       290: 987888876, 291: 880440844, 292: 257046104, 293: 880097232, 294: 239556546, 295: 932541092, 296: 761345504,
       297: 294032033, 298: 88374595, 299: 92626893, 300: 847522182, 301: 680606814, 302: 654389591, 303: 539232924,
       304: 827576667, 305: 729781323, 306: 761631041, 307: 433023392, 308: 296818150, 309: 677676208, 310: 968426260,
       311: 52987960, 312: 118222041, 313: 820886451, 314: 930557566, 315: 678484032, 316: 471304706, 317: 130480056,
       318: 555095809, 319: 535251483, 320: 594199346, 321: 582944431, 322: 649285983, 323: 653977171, 324: 795986361,
       325: 122479646, 326: 414858621, 327: 387286493, 328: 325252367, 329: 622944932, 330: 932932795, 331: 724276198,
       332: 134022793, 333: 576284423, 334: 643642230, 335: 18622334, 336: 998302327, 337: 915483394, 338: 662250830,
       339: 974122536, 340: 221592040, 341: 938088156, 342: 762404339, 343: 90104181, 344: 896477943, 345: 396851790,
       346: 344208589, 347: 474853230, 348: 893430284, 349: 416011300, 350: 573729924, 351: 597685837, 352: 29445989,
       353: 594284957, 354: 993844174, 355: 67213131, 356: 231428054, 357: 532763738, 358: 957150477, 359: 201162079,
       360: 983276350, 361: 142916537, 362: 667479369, 363: 156088144, 364: 70108417, 365: 887427347, 366: 731967836,
       367: 303545870, 368: 137079603, 369: 35669483, 370: 997428259, 371: 653172176, 372: 235249503, 373: 552856605,
       374: 719522600, 375: 564852003, 376: 177693296, 377: 44116170, 378: 651193107, 379: 799310570, 380: 334475144,
       381: 624668527, 382: 128793577, 383: 952539949, 384: 167064546, 385: 602256196, 386: 229081774, 387: 483932315,
       388: 972661761, 389: 861436589, 390: 368136560, 391: 652874003, 392: 391097583, 393: 457189577, 394: 272958082,
       395: 280253851, 396: 63542335, 397: 201872071, 398: 690754809, 399: 230402276, 400: 708332165, 401: 11203707,
       402: 410454124, 403: 994937135, 404: 133802574, 405: 147202474, 406: 237080588, 407: 726474032, 408: 691496513,
       409: 327935017, 410: 481443806, 411: 485414304, 412: 758639890, 413: 578417720, 414: 250141679, 415: 628956146,
       416: 399378044, 417: 849927562, 418: 338677566, 419: 27958627, 420: 903041039, 421: 792162775, 422: 140152825,
       423: 559291560, 424: 11217187, 425: 477026626, 426: 201885524, 427: 576730743, 428: 853970729, 429: 818139235,
       430: 275032190, 431: 664287742, 432: 230453578, 433: 611525693, 434: 218012689, 435: 813396049, 436: 156429092,
       437: 921923102, 438: 161557399, 439: 157699537, 440: 382892775, 441: 697420957, 442: 851408303, 443: 802540105,
       444: 177708213, 445: 247034018, 446: 770025918, 447: 77412535, 448: 200435946, 449: 433872116, 450: 817301181,
       451: 300828811, 452: 468335212, 453: 738474507, 454: 217454532, 455: 189714384, 456: 436627499, 457: 82828178,
       458: 775153729, 459: 150003729, 460: 260802653, 461: 966000513, 462: 866400598, 463: 692818235, 464: 488105874,
       465: 546020743, 466: 961399377, 467: 120993857, 468: 557336150, 469: 583285107, 470: 779627256, 471: 137030974,
       472: 132939191, 473: 390281005, 474: 842663056, 475: 436119329, 476: 627006908, 477: 269913443, 478: 584351944,
       479: 283205105, 480: 846314401, 481: 354240182, 482: 235308687, 483: 931484649, 484: 599124594, 485: 299400836,
       486: 58786587, 487: 552905755, 488: 7201658, 489: 878633151, 490: 608624504, 491: 165762041, 492: 720142921,
       493: 200708531, 494: 888632024, 495: 684432596, 496: 48679082, 497: 187939049, 498: 18945545, 499: 247836860,
       500: 763186505, 501: 756640569, 502: 364299760, 503: 211603283, 504: 951146619, 505: 82037858, 506: 771293555,
       507: 252479409, 508: 915656213, 509: 634532252, 510: 839153767, 511: 745784750, 512: 481120814, 513: 650537514,
       514: 96052781, 515: 618832550, 516: 764661482, 517: 930400051, 518: 357122404, 519: 95225177, 520: 729082088,
       521: 88769080, 522: 545430381, 523: 40009458, 524: 405044341, 525: 313595038, 526: 341113302, 527: 523893557,
       528: 558761494, 529: 794752181, 530: 254523077, 531: 460203746, 532: 64962433, 533: 903513764, 534: 323162773,
       535: 616510469, 536: 49219072, 537: 482490493, 538: 236397266, 539: 22249752, 540: 156654724, 541: 564108900,
       542: 682794186, 543: 580695586, 544: 803513954, 545: 315089621, 546: 893934455, 547: 10642314, 548: 857356914,
       549: 167908730, 550: 804307451, 551: 669794651, 552: 710347824, 553: 659010180, 554: 788243853, 555: 504122988,
       556: 837892597, 557: 283829965, 558: 681252014, 559: 384692679, 560: 403771101, 561: 256329995, 562: 770267642,
       563: 775814136, 564: 462312536, 565: 626246169, 566: 416239083, 567: 680980212, 568: 100981039, 569: 764035827,
       570: 820283571, 571: 561119278, 572: 635598874, 573: 642429889, 574: 716346503, 575: 673710767, 576: 585545109,
       577: 159512897, 578: 320221646, 579: 691535384, 580: 582655148, 581: 759278895, 582: 96094070, 583: 126458316,
       584: 679851604, 585: 330361793, 586: 835617501, 587: 488175700, 588: 544537986, 589: 94058914, 590: 935302690,
       591: 839412420, 592: 565313009, 593: 801349948, 594: 739642325, 595: 344158065, 596: 600039492, 597: 387478147,
       598: 877658928, 599: 416531113, 600: 67104160, 601: 425522420, 602: 80132874, 603: 911360923, 604: 910749764,
       605: 169229937, 606: 377269260, 607: 518853779, 608: 939730456, 609: 430290852, 610: 455809304, 611: 89208609,
       612: 507866231, 613: 623167869, 614: 358280721, 615: 734599152, 616: 93568568, 617: 612466784, 618: 428770437,
       619: 971569181, 620: 583903466, 621: 274753541, 622: 414232473, 623: 859579437, 624: 384714643, 625: 307193815,
       626: 103222023, 627: 10722882, 628: 283222908, 629: 396438412, 630: 65738016, 631: 902949813, 632: 800349308,
       633: 492601636, 634: 575015997, 635: 941670165, 636: 690641471, 637: 443934213, 638: 909268308, 639: 653530393,
       640: 561435761, 641: 800395666, 642: 293387352, 643: 647061600, 644: 764886025, 645: 171675135, 646: 27910692,
       647: 226450064, 648: 397172505, 649: 888919163, 650: 379044773, 651: 784618120, 652: 270524054, 653: 240084457,
       654: 471162379, 655: 110152560, 656: 927641847, 657: 13318688, 658: 829429870, 659: 237889004, 660: 580724498,
       661: 265117197, 662: 525120611, 663: 615112602, 664: 510165206, 665: 880604249, 666: 82543151, 667: 9328948,
       668: 110289165, 669: 210132153, 670: 11953859, 671: 432449988, 672: 132310151, 673: 700091291, 674: 72425129,
       675: 91935871, 676: 283243302, 677: 175629715, 678: 390344977, 679: 500459012, 680: 723651402, 681: 459159403,
       682: 74811029, 683: 728163878, 684: 144525418, 685: 727673582, 686: 457046765, 687: 166400305, 688: 335228618,
       689: 670941465, 690: 334107124, 691: 635173452, 692: 169286224, 693: 66492254, 694: 448905744, 695: 249816499,
       696: 643967437, 697: 457251868, 698: 14433286, 699: 751316111, 700: 992711436, 701: 55940899, 702: 433636397,
       703: 872218323, 704: 477199669, 705: 865668651, 706: 445361721, 707: 101743194, 708: 191467005, 709: 490776747,
       710: 461001264, 711: 408421970, 712: 844729923, 713: 855325283, 714: 262567689, 715: 69341428, 716: 107837827,
       717: 915470621, 718: 753500487, 719: 398057416, 720: 670102907, 721: 271931597, 722: 774813339, 723: 746523368,
       724: 356832220, 725: 381218905, 726: 977512994, 727: 145108116, 728: 190243343, 729: 220265847, 730: 199539171,
       731: 75990882, 732: 823601298, 733: 626029811, 734: 480889661, 735: 961789883, 736: 8301090, 737: 355444558,
       738: 727372538, 739: 165308520, 740: 106936430, 741: 476895882, 742: 900605543, 743: 536373378, 744: 226140099,
       745: 125203650, 746: 328526983, 747: 277838136, 748: 726333493, 749: 652158427, 750: 419653012, 751: 502684148,
       752: 197535394, 753: 510225952, 754: 712403393, 755: 731991345, 756: 924914228, 757: 464815608, 758: 545852942,
       759: 96643393, 760: 748149186, 761: 695997133, 762: 971338990, 763: 461261055, 764: 679474785, 765: 312427170,
       766: 410953302, 767: 152391264, 768: 482324573, 769: 352877896, 770: 548501870, 771: 915072274, 772: 731433600,
       773: 795748527, 774: 317865366, 775: 209677918, 776: 809670542, 777: 884810366, 778: 270238286, 779: 481068909,
       780: 722036135, 781: 721295416, 782: 511889380, 783: 192079592, 784: 780167543, 785: 471164374, 786: 1611720,
       787: 597037396, 788: 332197898, 789: 841631656, 790: 839713510, 791: 596283609, 792: 234191997, 793: 967455968,
       794: 764699880, 795: 852262894, 796: 676825738, 797: 951397957, 798: 404581219, 799: 425316970, 800: 308110020,
       801: 981505445, 802: 594247360, 803: 252298226, 804: 234863785, 805: 135582059, 806: 13511943, 807: 332996430,
       808: 920490921, 809: 635083101, 810: 428578226, 811: 314398694, 812: 824117448, 813: 600545334, 814: 229051401,
       815: 760703174, 816: 619964053, 817: 423756656, 818: 188595874, 819: 6206977, 820: 164143802, 821: 419145252,
       822: 594800889, 823: 852211917, 824: 328822026, 825: 504795474, 826: 900603014, 827: 976647777, 828: 91013472,
       829: 31130826, 830: 907804643, 831: 801364863, 832: 163579287, 833: 627533698, 834: 213168765, 835: 57241717,
       836: 805693863, 837: 852611829, 838: 905277558, 839: 645873465, 840: 832803900, 841: 488561422, 842: 104708631,
       843: 427945079, 844: 219657406, 845: 20271719, 846: 909301235, 847: 969805148, 848: 69389014, 849: 53081374,
       850: 244260368, 851: 383696981, 852: 795707624, 853: 123964056, 854: 264867891, 855: 467298776, 856: 617089563,
       857: 213894344, 858: 616680686, 859: 70067598, 860: 731391297, 861: 480981184, 862: 669731511, 863: 97744350,
       864: 397536611, 865: 570138654, 866: 432346540, 867: 932707434, 868: 969194467, 869: 81449066, 870: 320019429,
       871: 696282598, 872: 989054103, 873: 139088008, 874: 536138771, 875: 460208423, 876: 440288502, 877: 408339227,
       878: 848239851, 879: 711675505, 880: 357887782, 881: 393138566, 882: 757581156, 883: 690925510, 884: 199686853,
       885: 967663382, 886: 937141201, 887: 608380601, 888: 145895369, 889: 71933721, 890: 547901802, 891: 591368207,
       892: 548856522, 893: 579934178, 894: 624271566, 895: 177270541, 896: 211837003, 897: 137947136, 898: 703802224,
       899: 262142816, 900: 230806445, 901: 869541755, 902: 544714795, 903: 680238416, 904: 501186071, 905: 201972903,
       906: 639510995, 907: 422878767, 908: 478923013, 909: 915079918, 910: 126432564, 911: 609019617, 912: 457565310,
       913: 448616090, 914: 73068835, 915: 715541516, 916: 5350838, 917: 30156662, 918: 841061098, 919: 727292408,
       920: 512273697, 921: 74621149, 922: 118780879, 923: 915420125, 924: 664118449, 925: 949915357, 926: 53430800,
       927: 234547230, 928: 365435659, 929: 805492679, 930: 324105069, 931: 202202649, 932: 767895552, 933: 773781122,
       934: 45560394, 935: 131152409, 936: 430437731, 937: 373279693, 938: 123643741, 939: 706007053, 940: 738554002,
       941: 948388398, 942: 475737839, 943: 382197359, 944: 171436305, 945: 248151296, 946: 489250035, 947: 329174151,
       948: 89253927, 949: 499433088, 950: 558943641, 951: 74495276, 952: 735111744, 953: 988275285, 954: 704272064,
       955: 247221982, 956: 938268455, 957: 297122452, 958: 501288213, 959: 948406500, 960: 51959093, 961: 941181364,
       962: 610830029, 963: 786475650, 964: 918343479, 965: 958992348, 966: 25636574, 967: 992658175, 968: 320247894,
       969: 214680964, 970: 386375458, 971: 304063354, 972: 905321389, 973: 874170756, 974: 813673761, 975: 634563631,
       976: 36661726, 977: 114595909, 978: 324142784, 979: 862998632, 980: 205044669, 981: 467425777, 982: 248006666,
       983: 519287069, 984: 879047640, 985: 26893355, 986: 767084072, 987: 312164235, 988: 883122461, 989: 689435491,
       990: 36456339, 991: 10490853, 992: 140951958, 993: 11471231, 994: 461329741, 995: 757938329, 996: 103441948,
       997: 216028713, 998: 118374501, 999: 945437056, 1000: 980357000}

print(ans[cin_int()])