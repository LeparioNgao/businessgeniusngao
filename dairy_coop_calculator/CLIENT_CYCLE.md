# Dairy Co-op Price Checker — Full Client Cycle

## Stage 1: Brief Analysis

**Problem:** The co-op manually calls or WhatsApp-sends each farmer the weekly milk buying price, and farmers need to calculate what they are owed.

**Deliverable:** A working command-line Python calculator where a farmer enters a name and litres supplied and receives a KES total.

**Deadline:** End of week.

**Unclear:**
- The preferred name-entry format.
- Where the current price is stored and how it is updated.
- Who changes the weekly price.
- Whether the tool should run in a terminal or another interface.
- Whether payment history is required.

**Reasonable assumptions:**
- A co-op manager will update one text file weekly.
- The first version will calculate only the current payment and will not store history.
- Names are entered by keyboard; no account or login system is required.

## Stage 2: Clarifying Question

> Hello, before I begin: where should the current buying price be stored? If it is already in a spreadsheet, I can read it directly. If the co-op manager enters it manually each week, a simple `price.txt` file will let them update the rate without changing the code.

**Assumption if there is no reply before work starts:** The current price will be stored in `price.txt`. If the co-op later provides a database or complex spreadsheet integration, the timeline will extend by one day.

## Stage 3: Proposal

**Subject: Proposal — Dairy Co-op Price Checker**

Hello,

I understand that the co-op wants a simple way to calculate each farmer's payment when the weekly buying price changes. I have seen that manual calls and WhatsApp messages are the current process.

I will build a command-line Python tool. The manager can update the weekly rate in `price.txt`, and a farmer can enter their name and litres supplied to receive an immediate payment total. The approach keeps the first version simple and avoids unnecessary website or database costs.

**Deliverables:** one working Python script, `price.txt`, setup and usage README, example output, and basic tests.

**Price and timeline:** KES 8,000, with delivery within the current week. Payment terms: 50% deposit (KES 4,000) before work begins and 50% (KES 4,000) on delivery. Revision scope is limited to the agreed calculator behaviour.

**Assumption:** the weekly price will be maintained in `price.txt`. Database or complex spreadsheet integration is outside this scope.

Shall I proceed? Thank you.

## Stage 4: Commented Build Process

1. Added `dairy_calculator.py` with a `get_current_price()` function.
2. Set `price.txt` beside the script as the weekly rate source.
3. Added positive-number and text validation for litres.
4. Added required-name validation.
5. Added a KES-formatted payment summary.
6. Added unit tests and tested invalid input behaviour.

## Stage 5: Delivery Message

Hello,

I have completed the Dairy Co-op Price Checker as agreed. The tool reads the weekly buying price from `price.txt`, accepts a farmer name and litres supplied, and calculates the payment in KES.

The delivery package includes:
- the working Python script;
- `price.txt`, initially set to KES 55.0 per litre;
- setup and usage instructions;
- example output; and
- automated tests.

The source is packaged at `dairy_coop_calculator/` and tagged for version 1.0. Please confirm delivery once you can run it. Thank you.

## Stage 6: Revision-Request Response

Hello, thank you — I'm glad the first version is working as agreed.

Adding a running log of every farmer's payment is a new feature rather than a bug fix, because payment history was not included in the original brief or delivery scope. I can quote it separately as an add-on. It would need decisions about storage, date/time fields, backup, export, and whether the month-end report should be CSV or printable text.

The current calculator remains complete under the original agreement. Once you confirm the preferred log format, I can provide a separate quote and timeline.

Thank you.
