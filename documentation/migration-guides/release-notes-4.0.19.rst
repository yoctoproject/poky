.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release notes for Yocto-4.0.19 (Kirkstone)
------------------------------------------

Security Fixes in Yocto-4.0.19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  bluez5: Fix :cve:`2023-27349`, :cve:`2023-50229` and :cve:`2023-50230`
-  ghostscript: Fix :cve:`2023-52722`, :cve_mitre:`2024-29510`, :cve_mitre:`2024-33869`, :cve_mitre:`2024-33870` and :cve_mitre:`2024-33871`
-  git: Fix :cve:`2024-32002`, :cve:`2024-32004`, :cve:`2024-32020`, :cve:`2024-32021` and :cve:`2024-32465`
-  glibc: Fix :cve:`2024-2961`, :cve:`2024-33599`, :cve:`2024-33600`, :cve:`2024-33601` and :cve:`2024-33602`
-  gnutls: Fix :cve:`2024-28834` and :cve:`2024-28835`
-  go: Fix :cve:`2023-45288`
-  gstreamer1.0-plugins-bad: Fix :cve:`2023-44446`, :cve:`2023-50186` and :cve_mitre:`2024-0444`
-  less: Fix :cve:`2024-32487`
-  libarchive: Fix :cve:`2024-26256`
-  libarchive: Fix multiple null deference and heap overflow in pax writer (no CVE assigned)
-  linux-yocto/5.15: Fix :cve:`2023-6270`, :cve:`2023-7042`, :cve:`2023-52447`, :cve:`2023-52620`, :cve:`2024-22099`, :cve:`2024-26622`, :cve:`2024-26651`, :cve:`2024-26659`, :cve:`2024-26688`, :cve:`2024-26782`, :cve:`2024-26787`, :cve:`2024-26788`, :cve:`2024-26790`, :cve:`2024-26791`, :cve:`2024-26793`, :cve:`2024-26795`, :cve:`2024-26798`, :cve:`2024-26801`, :cve:`2024-26802`, :cve:`2024-26803`, :cve:`2024-26804`, :cve:`2024-26805` and :cve:`2024-26809`
-  linux-yocto/5.15: Ignore :cve:`2019-25160`, :cve:`2019-25162`, :cve:`2020-36775`, :cve:`2020-36776`, :cve:`2020-36777`, :cve:`2020-36778`, :cve:`2020-36779`, :cve:`2020-36780`, :cve:`2020-36781`, :cve:`2020-36782`, :cve:`2020-36783`, :cve:`2020-36784`, :cve:`2020-36785`, :cve:`2020-36786`, :cve:`2020-36787`, :cve:`2021-46904`, :cve:`2021-46905`, :cve:`2021-46906`, :cve:`2021-46908`, :cve:`2021-46909`, :cve:`2021-46910`, :cve:`2021-46911`, :cve:`2021-46912`, :cve:`2021-46913`, :cve:`2021-46914`, :cve:`2021-46915`, :cve:`2021-46916`, :cve:`2021-46917`, :cve:`2021-46918`, :cve:`2021-46919`, :cve:`2021-46920`, :cve:`2021-46921`, :cve:`2021-46922`, :cve:`2021-46923`, :cve:`2021-46924`, :cve:`2021-46925`, :cve:`2021-46926`, :cve:`2021-46927`, :cve:`2021-46928`, :cve:`2021-46929`, :cve:`2021-46930`, :cve:`2021-46931`, :cve:`2021-46932`, :cve:`2021-46933`, :cve:`2021-46934`, :cve:`2021-46935`, :cve:`2021-46936`, :cve:`2021-46937`, :cve:`2021-46938`, :cve:`2021-46939`, :cve:`2021-46940`, :cve:`2021-46941`, :cve:`2021-46942`, :cve:`2021-46943`, :cve:`2021-46944`, :cve:`2021-46945`, :cve:`2021-46947`, :cve:`2021-46948`, :cve:`2021-46949`, :cve:`2021-46950`, :cve:`2021-46951`, :cve:`2021-46952`, :cve:`2021-46953`, :cve:`2021-46954`, :cve:`2021-46955`, :cve:`2021-46956`, :cve:`2021-46957`, :cve:`2021-46958`, :cve:`2021-46959`, :cve:`2021-46960`, :cve:`2021-46961`, :cve:`2021-46962`, :cve:`2021-46963`, :cve:`2021-46964`, :cve:`2021-46965`, :cve:`2021-46966`, :cve:`2021-46967`, :cve:`2021-46968`, :cve:`2021-46969`, :cve:`2021-46970`, :cve:`2021-46971`, :cve:`2021-46972`, :cve:`2021-46973`, :cve:`2021-46974`, :cve:`2021-46976`, :cve:`2021-46977`, :cve:`2021-46978`, :cve:`2021-46979`, :cve:`2021-46980`, :cve:`2021-46981`, :cve:`2021-46982`, :cve:`2021-46983`, :cve:`2021-46984`, :cve:`2021-46985`, :cve:`2021-46986`, :cve:`2021-46987`, :cve:`2021-46988`, :cve:`2021-46989`, :cve:`2021-46990`, :cve:`2021-46991`, :cve:`2021-46992`, :cve:`2021-46993`, :cve:`2021-46994`, :cve:`2021-46995`, :cve:`2021-46996`, :cve:`2021-46997`, :cve:`2021-46998`, :cve:`2021-46999`, :cve:`2021-47000`, :cve:`2021-47001`, :cve:`2021-47002`, :cve:`2021-47003`, :cve:`2021-47004`, :cve:`2021-47005`, :cve:`2021-47006`, :cve:`2021-47007`, :cve:`2021-47008`, :cve:`2021-47009`, :cve:`2021-47010`, :cve:`2021-47011`, :cve:`2021-47012`, :cve:`2021-47013`, :cve:`2021-47014`, :cve:`2021-47015`, :cve:`2021-47016`, :cve:`2021-47017`, :cve:`2021-47018`, :cve:`2021-47019`, :cve:`2021-47020`, :cve:`2021-47021`, :cve:`2021-47022`, :cve:`2021-47023`, :cve:`2021-47024`, :cve:`2021-47025`, :cve:`2021-47026`, :cve:`2021-47027`, :cve:`2021-47028`, :cve:`2021-47029`, :cve:`2021-47030`, :cve:`2021-47031`, :cve:`2021-47032`, :cve:`2021-47033`, :cve:`2021-47034`, :cve:`2021-47035`, :cve:`2021-47036`, :cve:`2021-47037`, :cve:`2021-47038`, :cve:`2021-47039`, :cve:`2021-47040`, :cve:`2021-47041`, :cve:`2021-47042`, :cve:`2021-47043`, :cve:`2021-47044`, :cve:`2021-47045`, :cve:`2021-47046`, :cve:`2021-47047`, :cve:`2021-47048`, :cve:`2021-47049`, :cve:`2021-47050`, :cve:`2021-47051`, :cve:`2021-47052`, :cve:`2021-47053`, :cve:`2021-47054`, :cve:`2021-47055`, :cve:`2021-47056`, :cve:`2021-47057`, :cve:`2021-47058`, :cve:`2021-47059`, :cve:`2021-47060`, :cve:`2021-47061`, :cve:`2021-47062`, :cve:`2021-47063`, :cve:`2021-47064`, :cve:`2021-47065`, :cve:`2021-47066`, :cve:`2021-47067`, :cve:`2021-47068`, :cve:`2021-47069`, :cve:`2021-47070`, :cve:`2021-47071`, :cve:`2021-47072`, :cve:`2021-47073`, :cve:`2021-47074`, :cve:`2021-47075`, :cve:`2021-47076`, :cve:`2021-47077`, :cve:`2021-47078`, :cve:`2021-47079`, :cve:`2021-47080`, :cve:`2021-47081`, :cve:`2021-47082`, :cve:`2021-47083`, :cve:`2021-47086`, :cve:`2021-47087`, :cve:`2021-47088`, :cve:`2021-47089`, :cve:`2021-47090`, :cve:`2021-47091`, :cve:`2021-47092`, :cve:`2021-47093`, :cve:`2021-47094`, :cve:`2021-47095`, :cve:`2021-47096`, :cve:`2021-47097`, :cve:`2021-47098`, :cve:`2021-47099`, :cve:`2021-47100`, :cve:`2021-47101`, :cve:`2021-47102`, :cve:`2021-47103`, :cve:`2021-47104`, :cve:`2021-47105`, :cve:`2021-47106`, :cve:`2021-47107`, :cve:`2021-47108`, :cve:`2021-47109`, :cve:`2021-47110`, :cve:`2021-47111`, :cve:`2021-47112`, :cve:`2021-47113`, :cve:`2021-47114`, :cve:`2021-47116`, :cve:`2021-47117`, :cve:`2021-47118`, :cve:`2021-47119`, :cve:`2021-47120`, :cve:`2021-47121`, :cve:`2021-47122`, :cve:`2021-47123`, :cve:`2021-47124`, :cve:`2021-47125`, :cve:`2021-47126`, :cve:`2021-47127`, :cve:`2021-47128`, :cve:`2021-47129`, :cve:`2021-47130`, :cve:`2021-47131`, :cve:`2021-47132`, :cve:`2021-47133`, :cve:`2021-47134`, :cve:`2021-47135`, :cve:`2021-47136`, :cve:`2021-47137`, :cve:`2021-47138`, :cve:`2021-47139`, :cve:`2021-47140`, :cve:`2021-47141`, :cve:`2021-47142`, :cve:`2021-47143`, :cve:`2021-47144`, :cve:`2021-47145`, :cve:`2021-47146`, :cve:`2021-47147`, :cve:`2021-47148`, :cve:`2021-47149`, :cve:`2021-47150`, :cve:`2021-47151`, :cve:`2021-47152`, :cve:`2021-47153`, :cve:`2021-47158`, :cve:`2021-47159`, :cve:`2021-47160`, :cve:`2021-47161`, :cve:`2021-47162`, :cve:`2021-47163`, :cve:`2021-47164`, :cve:`2021-47165`, :cve:`2021-47166`, :cve:`2021-47167`, :cve:`2021-47168`, :cve:`2021-47169`, :cve:`2021-47170`, :cve:`2021-47171`, :cve:`2021-47172`, :cve:`2021-47173`, :cve:`2021-47174`, :cve:`2021-47175`, :cve:`2021-47176`, :cve:`2021-47177`, :cve:`2021-47178`, :cve:`2021-47179` and :cve:`2021-47180`
-  linux-yocto/5.15 (cont.): Ignore :cve:`2022-48626`, :cve:`2022-48627`, :cve:`2022-48629`, :cve:`2022-48630`, :cve:`2023-6356`, :cve:`2023-6536`, :cve:`2023-52434`, :cve:`2023-52465`, :cve:`2023-52467`, :cve:`2023-52468`, :cve:`2023-52469`, :cve:`2023-52470`, :cve:`2023-52471`, :cve:`2023-52472`, :cve:`2023-52473`, :cve:`2023-52474`, :cve:`2023-52475`, :cve:`2023-52476`, :cve:`2023-52477`, :cve:`2023-52478`, :cve:`2023-52479`, :cve:`2023-52480`, :cve:`2023-52482`, :cve:`2023-52483`, :cve:`2023-52484`, :cve:`2023-52486`, :cve:`2023-52487`, :cve:`2023-52489`, :cve:`2023-52490`, :cve:`2023-52491`, :cve:`2023-52492`, :cve:`2023-52493`, :cve:`2023-52494`, :cve:`2023-52495`, :cve:`2023-52497`, :cve:`2023-52498`, :cve:`2023-52499`, :cve:`2023-52500`, :cve:`2023-52501`, :cve:`2023-52502`, :cve:`2023-52503`, :cve:`2023-52504`, :cve:`2023-52505`, :cve:`2023-52507`, :cve:`2023-52509`, :cve:`2023-52510`, :cve:`2023-52511`, :cve:`2023-52512`, :cve:`2023-52513`, :cve:`2023-52515`, :cve:`2023-52516`, :cve:`2023-52517`, :cve:`2023-52518`, :cve:`2023-52519`, :cve:`2023-52520`, :cve:`2023-52522`, :cve:`2023-52523`, :cve:`2023-52524`, :cve:`2023-52525`, :cve:`2023-52526`, :cve:`2023-52527`, :cve:`2023-52528`, :cve:`2023-52529`, :cve:`2023-52531`, :cve:`2023-52559`, :cve:`2023-52560`, :cve:`2023-52562`, :cve:`2023-52563`, :cve:`2023-52564`, :cve:`2023-52566`, :cve:`2023-52567`, :cve:`2023-52570`, :cve:`2023-52573`, :cve:`2023-52574`, :cve:`2023-52575`, :cve:`2023-52577`, :cve:`2023-52578`, :cve:`2023-52580`, :cve:`2023-52581`, :cve:`2023-52583`, :cve:`2023-52587`, :cve:`2023-52588`, :cve:`2023-52594`, :cve:`2023-52595`, :cve:`2023-52597`, :cve:`2023-52598`, :cve:`2023-52599`, :cve:`2023-52600`, :cve:`2023-52601`, :cve:`2023-52602`, :cve:`2023-52603`, :cve:`2023-52604`, :cve:`2023-52606`, :cve:`2023-52607`, :cve:`2023-52608`, :cve:`2023-52609`, :cve:`2023-52610`, :cve:`2023-52611`, :cve:`2023-52612`, :cve:`2023-52613`, :cve:`2023-52614`, :cve:`2023-52615`, :cve:`2023-52616`, :cve:`2023-52617`, :cve:`2023-52618`, :cve:`2023-52619`, :cve:`2023-52622`, :cve:`2023-52623`, :cve:`2023-52626`, :cve:`2023-52627`, :cve:`2023-52628`, :cve:`2023-52630`, :cve:`2023-52631`, :cve:`2023-52633`, :cve:`2023-52635`, :cve:`2023-52636`, :cve:`2023-52637`, :cve:`2023-52638`, :cve:`2023-52640`, :cve:`2023-52641`, :cve:`2024-0565`, :cve:`2024-0841`, :cve:`2024-23196`, :cve:`2024-26587`, :cve:`2024-26588`, :cve:`2024-26600`, :cve:`2024-26601`, :cve:`2024-26602`, :cve:`2024-26603`, :cve:`2024-26604`, :cve:`2024-26605`, :cve:`2024-26606`, :cve:`2024-26608`, :cve:`2024-26610`, :cve:`2024-26611`, :cve:`2024-26612`, :cve:`2024-26614`, :cve:`2024-26615`, :cve:`2024-26616`, :cve:`2024-26617`, :cve:`2024-26618`, :cve:`2024-26619`, :cve:`2024-26620`, :cve:`2024-26621`, :cve:`2024-26625`, :cve:`2024-26626`, :cve:`2024-26627`, :cve:`2024-26629`, :cve:`2024-26630`, :cve:`2024-26631`, :cve:`2024-26632`, :cve:`2024-26633`, :cve:`2024-26634`, :cve:`2024-26635`, :cve:`2024-26636`, :cve:`2024-26637`, :cve:`2024-26638`, :cve:`2024-26639`, :cve:`2024-26640`, :cve:`2024-26641`, :cve:`2024-26643`, :cve:`2024-26644`, :cve:`2024-26645`, :cve:`2024-26649`, :cve:`2024-26652`, :cve:`2024-26653`, :cve:`2024-26657`, :cve:`2024-26660`, :cve:`2024-26663`, :cve:`2024-26664`, :cve:`2024-26665`, :cve:`2024-26666`, :cve:`2024-26667`, :cve:`2024-26668`, :cve:`2024-26670`, :cve:`2024-26671`, :cve:`2024-26673`, :cve:`2024-26674`, :cve:`2024-26675`, :cve:`2024-26676`, :cve:`2024-26678`, :cve:`2024-26679`, :cve:`2024-26681`, :cve:`2024-26682`, :cve:`2024-26683`, :cve:`2024-26684`, :cve:`2024-26685`, :cve:`2024-26689`, :cve:`2024-26690`, :cve:`2024-26692`, :cve:`2024-26693`, :cve:`2024-26694`, :cve:`2024-26695`, :cve:`2024-26696`, :cve:`2024-26697`, :cve:`2024-26698`, :cve:`2024-26702`, :cve:`2024-26703`, :cve:`2024-26704`, :cve:`2024-26705`, :cve:`2024-26707`, :cve:`2024-26708`, :cve:`2024-26709`, :cve:`2024-26710`, :cve:`2024-26711`, :cve:`2024-26712`, :cve:`2024-26715`, :cve:`2024-26716`, :cve:`2024-26717`, :cve:`2024-26720`, :cve:`2024-26721`, :cve:`2024-26722`, :cve:`2024-26723`, :cve:`2024-26724`, :cve:`2024-26725`, :cve:`2024-26727`, :cve:`2024-26728`, :cve:`2024-26729`, :cve:`2024-26730`, :cve:`2024-26731`, :cve:`2024-26732`, :cve:`2024-26733`, :cve:`2024-26734`, :cve:`2024-26735`, :cve:`2024-26736`, :cve:`2024-26737`, :cve:`2024-26741`, :cve:`2024-26742`, :cve:`2024-26743`, :cve:`2024-26744`, :cve:`2024-26746`, :cve:`2024-26747`, :cve:`2024-26748`, :cve:`2024-26749`, :cve:`2024-26750`, :cve:`2024-26751`, :cve:`2024-26752`, :cve:`2024-26753`, :cve:`2024-26754`, :cve:`2024-26755`, :cve:`2024-26760`, :cve:`2024-26761`, :cve:`2024-26762`, :cve:`2024-26763`, :cve:`2024-26764`, :cve:`2024-26766`, :cve:`2024-26769`, :cve:`2024-26771`, :cve:`2024-26772`, :cve:`2024-26773`, :cve:`2024-26774`, :cve:`2024-26776`, :cve:`2024-26777`, :cve:`2024-26778`, :cve:`2024-26779`, :cve:`2024-26780`, :cve:`2024-26781`, :cve:`2024-26783`, :cve:`2024-26785`, :cve:`2024-26786`, :cve:`2024-26792`, :cve:`2024-26794`, :cve:`2024-26796`, :cve:`2024-26799`, :cve:`2024-26800`, :cve:`2024-26807` and :cve:`2024-26808`
-  ncurses: Fix :cve:`2023-45918`
-  ofono: Fix :cve:`2023-4233` and :cve:`2023-4234`
-  openssl: Fix :cve:`2024-4603`
-  util-linux: Fix :cve:`2024-28085`
-  xserver-xorg: Fix :cve:`2024-31082` and :cve:`2024-31083`


Fixes in Yocto-4.0.19
~~~~~~~~~~~~~~~~~~~~~

-  binutils: Rename CVE-2022-38126 patch to :cve:`2022-35205`
-  bitbake: parse: Improve/fix cache invalidation via mtime
-  build-appliance-image: Update to kirkstone head revision
-  go-mod.bbclass: do not pack go mod cache
-  dev-manual: update custom distribution section
-  docs: poky.yaml.in: drop mesa/sdl from essential host packages
-  docs: standards.md: align with master branch
-  glibc: Update to latest on stable 2.35 branch (54a666dc5c...)
-  go.bbclass: fix path to linker in native Go builds
-  go.bbclass: Always pass interpreter to linker
-  initscripts: Add custom mount args for /var/lib
-  kernel.bbclass: check if directory exists before removing empty module directory
-  libpciaccess: Remove duplicated license entry
-  linux-yocto/5.15: cfg: remove obselete CONFIG_NFSD_V3 option
-  linux-yocto/5.15: update to v5.15.157
-  migration-notes: add release notes for 4.0.18
-  poky.conf: bump version for 4.0.19
-  ppp: Add RSA-MD in :term:`LICENSE`
-  python3: Upgrade to 3.10.14
-  ref-manual: update releases.svg
-  ref-manual: variables: Update default :term:`INHERIT_DISTRO` value
-  rootfs-postcommands.bbclass: Only set DROPBEAR_RSAKEY_DIR once
-  systemd-systemctl: Fix WantedBy processing


Known Issues in Yocto-4.0.19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- N/A


Contributors to Yocto-4.0.19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Alexander Kanavin
-  Archana Polampalli
-  Bhabu Bindu
-  Bob Henz
-  Bruce Ashfield
-  Colin McAllister
-  Dmitry Baryshkov
-  Geoff Parker
-  Heiko Thole
-  Joerg Vehlow
-  Lee Chee Yang
-  Michael Glembotzki
-  Michael Opdenacker
-  Paul Eggleton
-  Peter Marko
-  Poonam Jadhav
-  Richard Purdie
-  Soumya Sambu
-  Stefan Herbrechtsmeier
-  Steve Sakoman
-  Vijay Anusuri
-  Yogita Urade


Repositories / Downloads for Yocto-4.0.19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

poky

-  Repository Location: :yocto_git:`/poky`
-  Branch: :yocto_git:`kirkstone </poky/log/?h=kirkstone>`
-  Tag:  :yocto_git:`yocto-4.0.19 </poky/log/?h=yocto-4.0.19>`
-  Git Revision: :yocto_git:`e139e9d0ce343ba77a09601a976c92acd562c9df </poky/commit/?id=e139e9d0ce343ba77a09601a976c92acd562c9df>`
-  Release Artefact: poky-e139e9d0ce343ba77a09601a976c92acd562c9df
-  sha: 3e568af60ee599e262a359b50446c6cbe239481d8be2ee55403bda497735d636
-  Download Locations:
   http://downloads.yoctoproject.org/releases/yocto/yocto-4.0.19/poky-e139e9d0ce343ba77a09601a976c92acd562c9df.tar.bz2
   http://mirrors.kernel.org/yocto/yocto/yocto-4.0.19/poky-e139e9d0ce343ba77a09601a976c92acd562c9df.tar.bz2

openembedded-core

-  Repository Location: :oe_git:`/openembedded-core`
-  Branch: :oe_git:`kirkstone </openembedded-core/log/?h=kirkstone>`
-  Tag:  :oe_git:`yocto-4.0.19 </openembedded-core/log/?h=yocto-4.0.19>`
-  Git Revision: :oe_git:`ab2649ef6c83f0ae7cac554a72e6bea4dcda0e99 </openembedded-core/commit/?id=ab2649ef6c83f0ae7cac554a72e6bea4dcda0e99>`
-  Release Artefact: oecore-ab2649ef6c83f0ae7cac554a72e6bea4dcda0e99
-  sha: abc7601650651a2d2260f7e7e9e2e0709f25233148d66cb2d9481775b7b59a0c
-  Download Locations:
   http://downloads.yoctoproject.org/releases/yocto/yocto-4.0.19/oecore-ab2649ef6c83f0ae7cac554a72e6bea4dcda0e99.tar.bz2
   http://mirrors.kernel.org/yocto/yocto/yocto-4.0.19/oecore-ab2649ef6c83f0ae7cac554a72e6bea4dcda0e99.tar.bz2

meta-mingw

-  Repository Location: :yocto_git:`/meta-mingw`
-  Branch: :yocto_git:`kirkstone </meta-mingw/log/?h=kirkstone>`
-  Tag:  :yocto_git:`yocto-4.0.19 </meta-mingw/log/?h=yocto-4.0.19>`
-  Git Revision: :yocto_git:`f6b38ce3c90e1600d41c2ebb41e152936a0357d7 </meta-mingw/commit/?id=f6b38ce3c90e1600d41c2ebb41e152936a0357d7>`
-  Release Artefact: meta-mingw-f6b38ce3c90e1600d41c2ebb41e152936a0357d7
-  sha: 7d57167c19077f4ab95623d55a24c2267a3a3fb5ed83688659b4c03586373b25
-  Download Locations:
   http://downloads.yoctoproject.org/releases/yocto/yocto-4.0.19/meta-mingw-f6b38ce3c90e1600d41c2ebb41e152936a0357d7.tar.bz2
   http://mirrors.kernel.org/yocto/yocto/yocto-4.0.19/meta-mingw-f6b38ce3c90e1600d41c2ebb41e152936a0357d7.tar.bz2

meta-gplv2

-  Repository Location: :yocto_git:`/meta-gplv2`
-  Branch: :yocto_git:`kirkstone </meta-gplv2/log/?h=kirkstone>`
-  Tag:  :yocto_git:`yocto-4.0.19 </meta-gplv2/log/?h=yocto-4.0.19>`
-  Git Revision: :yocto_git:`d2f8b5cdb285b72a4ed93450f6703ca27aa42e8a </meta-gplv2/commit/?id=d2f8b5cdb285b72a4ed93450f6703ca27aa42e8a>`
-  Release Artefact: meta-gplv2-d2f8b5cdb285b72a4ed93450f6703ca27aa42e8a
-  sha: c386f59f8a672747dc3d0be1d4234b6039273d0e57933eb87caa20f56b9cca6d
-  Download Locations:
   http://downloads.yoctoproject.org/releases/yocto/yocto-4.0.19/meta-gplv2-d2f8b5cdb285b72a4ed93450f6703ca27aa42e8a.tar.bz2
   http://mirrors.kernel.org/yocto/yocto/yocto-4.0.19/meta-gplv2-d2f8b5cdb285b72a4ed93450f6703ca27aa42e8a.tar.bz2

bitbake

-  Repository Location: :oe_git:`/bitbake`
-  Branch: :oe_git:`2.0 </bitbake/log/?h=2.0>`
-  Tag:  :oe_git:`yocto-4.0.19 </bitbake/log/?h=yocto-4.0.19>`
-  Git Revision: :oe_git:`5a90927f31c4f9fccbe5d9d07d08e6e69485baa8 </bitbake/commit/?id=5a90927f31c4f9fccbe5d9d07d08e6e69485baa8>`
-  Release Artefact: bitbake-5a90927f31c4f9fccbe5d9d07d08e6e69485baa8
-  sha: e64b7f747718d10565d733057a8e6ee592c6b64983c7ffe623f9315ad35b6e0c
-  Download Locations:
   http://downloads.yoctoproject.org/releases/yocto/yocto-4.0.19/bitbake-5a90927f31c4f9fccbe5d9d07d08e6e69485baa8.tar.bz2
   http://mirrors.kernel.org/yocto/yocto/yocto-4.0.19/bitbake-5a90927f31c4f9fccbe5d9d07d08e6e69485baa8.tar.bz2

yocto-docs

-  Repository Location: :yocto_git:`/yocto-docs`
-  Branch: :yocto_git:`kirkstone </yocto-docs/log/?h=kirkstone>`
-  Tag: :yocto_git:`yocto-4.0.19 </yocto-docs/log/?h=yocto-4.0.19>`
-  Git Revision: :yocto_git:`78b8d5b18274a41ffec43ca4e136abc717585f6d </yocto-docs/commit/?id=78b8d5b18274a41ffec43ca4e136abc717585f6d>`

