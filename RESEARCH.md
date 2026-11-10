# RESEARCH — TapeOut / X Layer / OKX event

Researched 9 Nov 2026. Every claim below is marked VERIFIED (read on the
source named) or UNVERIFIED (not yet established — do not build on it
until checked). Nothing here is copied from a secondary summary without
saying so.

## 1. The event — VERIFIED (official OKX page)

Source: https://web3.okx.com/xlayer/build-x-series
("Crypto Hackathon 2026 | OKX Web3 Developer Challenge", X Layer
TapeOut Accelerate section) — full page text fetched 9 Nov 2026,
crawled 07:49 UTC the same day.

| Claim | Status |
|---|---|
| 100,000 USDT pool: 1st 20,000 / 2nd 10,000 ×5 / 3rd 6,000 ×5 | VERIFIED (page prize table) |
| Pool "will continue to grow" with founder/team/community contributions | VERIFIED (page text) |
| Deadline: submit before **7 Dec 2026, 23:59 UTC = 8 Dec 05:29 IST** | VERIFIED (page text); **provisional** — "the official event page will confirm the final date" |
| Must build within the TapeOut ecosystem AND either use TapeOut circuits, contracts, or onchain data on X Layer, OR run on X Layer DeWEB | VERIFIED (requirements) |
| Eligible directions: apps, games, online services, developer tools, circuit design, PoD mechanisms; real Web2/Web3 needs encouraged; building on existing ecosystem tools welcome | VERIFIED |
| Description must explain: product/service, target users + how to reach them, revenue model, why users pay and keep using. Circuit/tool/mechanism projects may explain use cases + commercial applications instead | VERIFIED |
| Circuit projects must submit processor contract address + circuit ID. Websites/apps/tools must provide an access link + explain which TapeOut ecosystem projects/features they use | VERIFIED |
| Existing projects eligible, but must include substantial new development during the event and describe it; only event work is judged | VERIFIED |
| Individuals and teams welcome; online; shortlisted teams attend an offline Demo Day | VERIFIED (Demo Day **location not stated** on the page) |
| Prizes paid **in stages** as winners work with X Layer + TapeOut to develop/grow projects; schedules/milestones agreed per team, after eligibility verification. Winners also get X Layer PR support + collaboration opportunities | VERIFIED (terms §6) |
| Judging: User Value + Commercial Potential; Innovation; Ecosystem Integration (DeWEB, FabX, TapeCode, TapeKit, TapeSend — "use of any specific project or tool is not required"); Product Readiness + UX; Demo Video ≤3 min recommended (problem, core features, target users + business model, how it uses TapeOut/ecosystem tools) | VERIFIED |
| FAQ: interfaces/computation may run outside circuits (explain which features use TapeOut); may build using existing TapeOut processors/circuits/dev tools (no need to design own circuit); revenue not required yet | VERIFIED (FAQ answers on the page; the page's text fetch shows answers without their questions — wording paraphrased, meaning checked against the requirements section) |
| Eligibility: 18+ or legal age of majority; "Restricted Persons under the X Layer Terms of Service are ineligible"; winners may face identity checks; recipient wallet must be self-custodial, user confirms address + network; organiser never asks for private keys/recovery phrases | VERIFIED (terms §3, §7, §8) |
| India excluded? | **NOT FOUND on the event page — no country list, no India mention.** Treat as "not excluded on the event page". The X Layer ToS restricted-persons list was NOT checked — see §5 unknowns |
| Submission form URL / field list | **UNVERIFIED — the page says "submit through the submission form" but the text fetch exposes no form link or field list.** Needs a live-browser check (parent task) |
| Event Telegram channel link ("join our Telegram channel" for inquiries/support) | **UNVERIFIED — link not captured in the text fetch.** Needs a live-browser check |
| "Learn more about TapeOut" link target | **UNVERIFIED — link not captured.** Presumably tapeout.net |

## 2. TapeOut protocol — MIXED (official site is JS-heavy; secondary sources)

Official site: https://tapeout.net/ — text fetch 9 Nov 2026 returned
almost nothing (Chinese landing line + legal notice only; the
processor catalogue loads from-chain via JS). What the fetch DID verify:

| Claim | Status |
|---|---|
| TapeOut is an open-source, non-custodial protocol; users interact with contracts via their own wallet; no financial/custody service | VERIFIED (tapeout.net legal notice) |
| Protocol v2.0 still in development, not deployed; factory contract currently upgradeable, controlled by a 3/5 multisig, only for new versions + security fixes | VERIFIED (tapeout.net legal notice) |
| Users must be of legal age, not sanctioned, and comply with local law | VERIFIED (tapeout.net legal notice) |

Secondary sources (use with care — community/press, not the protocol):

| Claim | Source | Status |
|---|---|---|
| Launched 15 Aug 2026 by developer Blonskr; NAND (logic) + LATCH (state) as onchain components; drag-and-drop Canvas; tape-out consumes components, records the netlist, mints a Circuit NFT; processors provide component supply; circuits reusable as black-box modules | bit.fan ecosystem piece; PANews beginner guide; Substack "Understanding TapeOut from Zero" | SECONDARY — consistent across 3 sources, not verified on tapeout.net itself |
| Combinational circuits readable via `eval(circuitId, bytes)`; sequential circuits via `step`; examples for BscScan Read Contract, CLI, ethers.js on the official site | PANews guide | SECONDARY — the eval/step interface is the key technical claim for our Tier-B circuit spike; MUST be verified hands-on in the Canvas in Week 2 before any claim is made |
| PoD (Proof of Design) mining; $BEM token, 21M supply, launched on BNB Chain 21 Aug 2026; BEM bridged 1:1 to X Layer (per a third-party monitor) | bit.fan; tapeout-public-monitor (third-party) | SECONDARY — irrelevant to our build except as context; we do not touch BEM |
| TapeKit = open-source browser kernel (GitHub TapeOutProtocol/TapeKit); TapeSend = DeWEB message layer (TAP-10); DeWEB = onchain websites whose files live in a circuit's container, replaceable by the circuit holder | TapeOut Complete Beginner's Guide v1.5 (community, 25 Sep 2026); third-party monitor | SECONDARY — DeWEB hosting model needs a hands-on check in Week 2 |
| FabX, TapeCode: named on the OKX page as ecosystem capabilities; what they do | OKX page names them only | UNVERIFIED — do not describe them until checked |
| Protocol now on three chains: BNB Chain, X Layer, Base | Third-party monitor | SECONDARY — X Layer presence is what matters; verify via the X Layer explorer in Week 2 |

### ⚠️ Name collision — VERIFIED (Bitrue blog, secondary)

**TAPEOUTX** (contract `0x16aa672dda63f5acd0de098c04c4a3e957d1eeee` on
X Layer) is a **different token** from TapeOut Protocol / **BEM**.
Do not cite the TAPEOUTX address, price, or docs as TapeOut Protocol
facts. Our project uses neither token.

## 3. X Layer — VERIFIED (multiple sources, consistent)

| Claim | Source | Status |
|---|---|---|
| Mainnet chain ID **196**, RPC `https://rpc.xlayer.tech`, gas **OKB**, explorer `web3.okx.com/explorer/x-layer` | OKX docs via Chainstack tooling docs (21 Oct 2026), Main.net, viem chain defs | VERIFIED (secondary, consistent across 4+ sources) |
| EVM-equivalent; standard Solidity / Hardhat / Foundry / ethers / viem work unchanged; Sourcify verification supported, no API key | Chainstack X Layer tooling docs | VERIFIED (secondary) |
| OP Stack (migrated from Polygon CDK zkEVM; re-genesis Oct 2025); ~1s blocks; trusted sequencer operated by OKX | Chainstack; Finst; AllSwap (reviewed 8 Nov 2026) | VERIFIED (secondary). Old "ZK" descriptions in 2024 launch coverage are STALE — do not cite |
| Testnet chain ID **1952**, testnet RPC `https://testrpc.xlayer.tech/terigon`, explorer `web3.okx.com/explorer/x-layer-testnet`, faucet `web3.okx.com/xlayer/faucet` | Chainstack tooling docs; Datawallet (Jun 2026) | VERIFIED (secondary, 2 sources agree on 1952). **Conflict noted:** older sources (BitGo, thirdweb 2024) cite testnet chain ID **195** — that was the old Sepolia testnet; 1952 is the current one. Faucet URL still needs a live check in Week 2 |
| Testnet OKB is free faucet gas with no monetary value | Thirdweb faucet guide; Chainstack | VERIFIED (secondary) |

## 4. Reused cores — VERIFIED (ran in this sandbox, 9 Nov 2026)

| Claim | Evidence |
|---|---|
| hermes-secret-gate: 42/42 tests PASS | `python3 -m unittest discover` in `nous-hermes/plugin`, Python 3.12.3, 0.024s |
| CageCheck policy engine: 10/10 tests PASS | `python3 -m unittest discover` in `cagecheck/tests`, Python 3.12.3 |
| No pytest / solc / Foundry in this sandbox | `which` check 9 Nov 2026 — contracts therefore uncompiled (stated, not hidden) |

## 5. Unknowns / blockers (for the parent + Week 2)

1. **Submission form URL + exact fields** — not exposed by the text
   fetch. Needs a live-browser visit to the OKX page.
2. **Telegram support channel link** — same.
3. **Demo Day location + date** — not on the event page.
4. **X Layer ToS restricted-persons list** — India eligibility is "not
   excluded on the event page" only; the ToS list must be checked
   before the submission claims India eligibility outright.
5. **TapeOut `eval(circuitId, bytes)` interface + Canvas flow** —
   secondary only; verify hands-on before the Tier-B circuit claim.
6. **DeWEB hosting steps** (TapeKit container deploy) — secondary
   only; verify hands-on.
7. **FabX / TapeCode** — what they are; may be useful, currently unknown.
8. **X Layer testnet faucet liveness** — URL known second-hand; claim
   test OKB only after a successful claim.
9. **TapeOut factory / processor contract addresses on X Layer** —
   none verified yet; needed for the submission's address fields.
