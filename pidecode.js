function RDSCall(obj)
{
	picode=obj.picode.value.toUpperCase()
	if (picode.substr(0,2)=="AF") {
		part1=picode.substr(2,2)
		part2="00"
		picode=part1+part2
	}
	if (picode.substr(0,1)=="A") {
		part1=picode.substr(1,1)
		part2="0"
		part3=picode.substr(2,2)
		picode=part1+part2+part3
	}
	picode=hex2dec(picode)
	csign="Bad code"
	if (picode>4095) {
		if (picode<39247) {
			if (picode>21671) {
				call1="W"
				code=picode-21672
			} else {
				call1="K"
				code=picode-4096
			}
			call2=getfloor(code/676)
			code=code-(676*call2)
			call3=getfloor(code/26)
			call4=code-(26*call3)
			csign2=chx(call2+65)
			csign3=chx(call3+65)
			csign4=chx(call4+65)
			csign=call1+csign2+csign3+csign4
		}
	}
			switch(picode) {
				case 49829:
					csign="CIMF";
					break;
				case 17185:
					csign="CJPT";
					break;
				case 39248:
					csign="KEX";
					break;
				case 39249:
					csign="KFH";
					break;

				case 39250:
					csign="KFI";
					break;

				case 39251:
					csign="KGA";
					break;

				case 39252:
					csign="KGO";
					break;

				case 39253:
					csign="KGU";
					break;

				case 39254:
					csign="KGW";
					break;

				case 39255:
					csign="KGY";
					break;

				case 39256:
					csign="KID";
					break;

				case 39257:
					csign="KIT";
					break;

				case 39258:
					csign="KJR";
					break;

				case 39259:
					csign="KLO";
					break;

				case 39260:
					csign="KLZ";
					break;

				case 39261:
					csign="KMA";
					break;

				case 39262:
					csign="KMJ";
					break;

				case 39263:
					csign="KNX";
					break;

				case 39264:
					csign="KOA";
					break;

				case 39268:
					csign="KQV";
					break;

				case 39269:
					csign="KSL";
					break;

				case 39270:
					csign="KUJ";
					break;

				case 39271:
					csign="KVI";
					break;

				case 39272:
					csign="KWG";
					break;

				case 39275:
					csign="KYW";
					break;

				case 39277:
					csign="WBZ";
					break;

				case 39278:
					csign="WDZ";
					break;

				case 39279:
					csign="WEW";
					break;

				case 39281:
					csign="WGL";
					break;

				case 39282:
					csign="WGN";
					break;

				case 39283:
					csign="WGR";
					break;

				case 39285:
					csign="WHA";
					break;

				case 39286:
					csign="WHB";
					break;

				case 39287:
					csign="WHK";
					break;

				case 39288:
					csign="WHO";
					break;

				case 39290:
					csign="WIP";
					break;

				case 39291:
					csign="WJR";
					break;

				case 39292:
					csign="WKY";
					break;

				case 39293:
					csign="WLS";
					break;

				case 39294:
					csign="WLW";
					break;

				case 39297:
					csign="WOC";
					break;

				case 39299:
					csign="WOL";
					break;

				case 39300:
					csign="WOR";
					break;

				case 39304:
					csign="WWJ";
					break;

				case 39305:
					csign="WWL";
					break;

				case 39312:
					csign="KDB";
					break;

				case 39313:
					csign="KGB";
					break;

				case 39314:
					csign="KOY";
					break;

				case 39315:
					csign="KPQ";
					break;

				case 39316:
					csign="KSD";
					break;

				case 39317:
					csign="KUT";
					break;

				case 39318:
					csign="KXL";
					break;

				case 39319:
					csign="KXO";
					break;

				case 39321:
					csign="WBT";
					break;

				case 39322:
					csign="WGH";
					break;

				case 39323:
					csign="WGY";
					break;

				case 39324:
					csign="WHP";
					break;

				case 39325:
					csign="WIL";
					break;

				case 39326:
					csign="WMC";
					break;

				case 39327:
					csign="WMT";
					break;

				case 39328:
					csign="WOI";
					break;

				case 39329:
					csign="WOW";
					break;

				case 39330:
					csign="WRR";
					break;

				case 39331:
					csign="WSB";
					break;

				case 39332:
					csign="WSM";
					break;

				case 39333:
					csign="KBW";
					break;

				case 39334:
					csign="KCY";
					break;
				case 39335:
					csign="KDF";
					break;
				case 39338:
					csign="KHQ";
					break;
				case 39339:
					csign="KOB";
					break;
				case 39347:
					csign="WIS";
					break;
				case 39348:
					csign="WJW";
					break;
				case 39349:
					csign="WJZ";
					break;
				case 39353:
					csign="WRC";
					break;
				case 26542:
					csign="WHFI/CHFI";
					break;
				case 39250:
					csign="KFI/CJBC";
					break;
				case 49160:
					csign="CJBC-1";
					break;
				case 49158:
					csign="CBCK";
					break;
				case 52010:
					csign="CBLG";
					break;
				case 52007:
					csign="CBLJ";
					break;
				case 52012:
					csign="CBQT";
					break;
				case 52009:
					csign="CBEB";
					break;
				case 28378:
					csign="WJXY/CJXY";
					break;
				case 39251:
					csign="KGA/CBCx";
					break;
				case 39252:
					csign="KGO/CBCP";
					break;
				case 941:
					csign="CKGE";
					break;
				case 16416:
					csign="KSFW/CBLA";
					break;
				case 25414:
					csign="WFNY/CFNY";
					break;
				case 27382:
					csign="WILQ/CILQ";
					break;
				case 27424:
					csign="WING/CING";
					break;
				case 26428:
					csign="WHAY/CHAY";
					break;
				case 52033:
					csign="CBA-FM";
					break;
				case 52034:
					csign="CBCT";
					break;
				case 52045:
					csign="CBHM";
					break;
				case 45084:
					csign="CIQM";
					break;
				case 51806:
					csign="CHNI, CJNI, or CKNI";
					break;
				case 12289:
					csign="KLAS (Jamaica)";
					break;
				case 7877:
					csign="CFPL";
					break;
				case 7760:
					csign="ZFKY (Cayman Is.)";
					break;
				case 8151:
					csign="ZFCC (Cayman Is.)";
					break;
				case 12656:
					csign="WAVW";
					break;
				case 7908:
					csign="KTCZ";
					break;
				case 42149:
					csign="KSKZ or KWKR";
					break;
				case 45313:
					csign="XHCTO";
					break;
				case 34784:
					csign="XHTRR";
					break;
				case 39333:
					csign="XHSR";
					break;
			}
	obj.csign.value=csign
}
