import sys
import math

codes = {49829: 'CIMF', 17185: 'CJPT', 39248: 'KEX', 39249: 'KFH', 39250: 'KFI/CJBC', 39251: 'KGA/CBCx', 39252: 'KGO/CBCP', 39253: 'KGU', 39254: 'KGW', 39255: 'KGY', 39256: 'KID', 39257: 'KIT', 39258: 'KJR', 39259: 'KLO', 39260: 'KLZ', 39261: 'KMA', 39262: 'KMJ', 39263: 'KNX', 39264: 'KOA', 39268: 'KQV', 39269: 'KSL', 39270: 'KUJ', 39271: 'KVI', 39272: 'KWG', 39275: 'KYW', 39277: 'WBZ', 39278: 'WDZ', 39279: 'WEW', 39281: 'WGL', 39282: 'WGN', 39283: 'WGR', 39285: 'WHA', 39286: 'WHB', 39287: 'WHK', 39288: 'WHO', 39290: 'WIP', 39291: 'WJR', 39292: 'WKY', 39293: 'WLS', 39294: 'WLW', 39297:'WOC', 39299: 'WOL', 39300: 'WOR', 39304: 'WWJ', 39305: 'WWL', 39312: 'KDB', 39313: 'KGB', 39314: 'KOY', 39315: 'KPQ', 39316: 'KSD', 39317: 'KUT', 39318: 'KXL', 39319: 'KXO', 39321: 'WBT', 39322: 'WGH', 39323: 'WGY', 39324: 'WHP', 39325: 'WIL', 39326: 'WMC', 39327: 'WMT', 39328: 'WOI', 39329: 'WOW', 39330: 'WRR', 39331: 'WSB', 39332: 'WSM', 39333: 'XHSR', 39334: 'KCY', 39335: 'KDF', 39338: 'KHQ', 39339: 'KOB', 39347: 'WIS', 39348: 'WJW', 39349: 'WJZ', 39353: 'WRC', 26542: 'WHFI/CHFI', 49160: 'CJBC-1', 49158: 'CBCK', 52010: 'CBLG', 52007: 'CBLJ', 52012: 'CBQT', 52009: 'CBEB', 28378: 'WJXY/CJXY', 941: 'CKGE', 16416: 'KSFW/CBLA', 25414: 'WFNY/CFNY', 27382: 'WILQ/CILQ', 27424: 'WING/CING', 26428: 'WHAY/CHAY', 52033: 'CBA-FM', 52034: 'CBCT', 52045: 'CBHM', 45084: 'CIQM', 51806: 'CHNI/CJNI/CKNI', 12289: 'KLAS', 7877: 'CFPL', 7760: 'ZFKY', 8151: 'ZFCC', 12656: 'WAVW', 7908: 'KTCZ', 42149: 'KSKZ or KWKR', 45313: 'XHCTO', 34784: 'XHTRR'}

codes[7601] = 'WJMN' # KFEV is wrong, as WJMN has a novelty callsign

def rdscall(code):
    picode = code.upper()
    if picode[0:2] == "AF":
        part1 = picode[2:4]
        part2 = "00"
        picode = picode[2:4] + "00"
    if picode[0] == "A":
        picode = picode[1] + "0" + picode[2:4]
    picode = int(picode, 16)
    if picode < 0:
        picode &= 0xffff
    csign = None
    call = []
    if picode > 4095:
        if picode < 39247:
            if picode > 21671:
                call.append("W")
                code = picode-21672
            else:
                call.append("K")
                code = picode-4096
            call.append(math.floor(code/676))
            code -= 676*call[-1]
            call.append(math.floor(code/26))
            call.append(code-26*call[-1])
            csign = call[0]+''.join([chr(x+65) for x in call[1:]])
        if picode in codes.keys():
            csign = codes[picode]
    return csign

if __name__ == "__main__":
    assert rdscall('A72F') == "WKLB"
    assert rdscall('64A1') == "WGBH"
    if len(sys.argv) == 2:
        print(rdscall(sys.argv[1]))
