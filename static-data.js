/*
  Figures that change once a year. Update this file each fall when the IRS
  publishes the next year's inflation adjustments (usually October/November),
  and in January for state rate changes. When you change figures, also update
  the matching "Data as of" label in the asOf block below.

  Sources
    Federal brackets, standard deduction: IRS Rev. Proc. 2025-32 (tax year 2026)
    Retirement/HSA limits: IRS Notice 2025-67 and Rev. Proc. 2025-19 (tax year 2026)
    State rates and brackets: Tax Foundation tables (Feb 17, 2026 and the April 28, 2026
      update in Facts & Figures 2026), plus 2026 laws passed after those tables for
      Arkansas, Georgia, Maine, South Carolina, Utah and West Virginia (state sources;
      see the stateBrackets comment below)
*/
window.STATIC = {
  taxYear: 2026,

  // "Data as of" labels shown under each hand-entered table on the page.
  // Change these whenever you update the figures below them.
  asOf: {
    brackets: { date: "Tax year 2026", source: "IRS Rev. Proc. 2025-32" },
    limits: { date: "Tax year 2026", source: "IRS Notice 2025-67 and Rev. Proc. 2025-19" },
    states: { date: "April 2026, plus later 2026 law changes in AR, GA, ME, SC, UT and WV", source: "Tax Foundation and state revenue agencies" },
  },

  // Each bracket is [rate %, top of bracket]. null = no upper limit.
  brackets: {
    single: {
      label: "Single",
      standardDeduction: 16100,
      rows: [[10, 12400], [12, 50400], [22, 105700], [24, 201775], [32, 256225], [35, 640600], [37, null]],
    },
    mfj: {
      label: "Married filing jointly",
      standardDeduction: 32200,
      rows: [[10, 24800], [12, 100800], [22, 211400], [24, 403550], [32, 512450], [35, 768700], [37, null]],
    },
    hoh: {
      label: "Head of household",
      standardDeduction: 24150,
      rows: [[10, 17700], [12, 67450], [22, 105700], [24, 201750], [32, 256200], [35, 640600], [37, null]],
    },
  },

  limits: [
    { name: "401(k), 403(b), most 457(b): employee deferral", limit: "$24,500", catchup: "$8,000 (age 50+); $11,250 (age 60\u201363)" },
    { name: "401(k) total, employee plus employer", limit: "$72,000", catchup: "\u2014" },
    { name: "Traditional or Roth IRA", limit: "$7,500", catchup: "$1,100 (age 50+)" },
    { name: "HSA, self-only coverage", limit: "$4,400", catchup: "$1,000 (age 55+)" },
    { name: "HSA, family coverage", limit: "$8,750", catchup: "$1,000 (age 55+)" },
  ],
  limitsFootnote:
    "Starting in 2026, higher earners must make 401(k) catch-up contributions as Roth contributions.",

  // [state, structure, top marginal rate %]. structure: none | flat | graduated
  states: [
    ["Alabama", "graduated", 5.0],
    ["Alaska", "none", 0],
    ["Arizona", "flat", 2.5],
    ["Arkansas", "graduated", 3.7],
    ["California", "graduated", 13.3],
    ["Colorado", "flat", 4.4],
    ["Connecticut", "graduated", 6.99],
    ["Delaware", "graduated", 6.6],
    ["District of Columbia", "graduated", 10.75],
    ["Florida", "none", 0],
    ["Georgia", "flat", 4.99],
    ["Hawaii", "graduated", 11.0],
    ["Idaho", "flat", 5.3],
    ["Illinois", "flat", 4.95],
    ["Indiana", "flat", 2.95],
    ["Iowa", "flat", 3.8],
    ["Kansas", "graduated", 5.58],
    ["Kentucky", "flat", 3.5],
    ["Louisiana", "flat", 3.0],
    ["Maine", "graduated", 9.15],
    ["Maryland", "graduated", 6.5],
    ["Massachusetts", "graduated", 9.0],
    ["Michigan", "flat", 4.25],
    ["Minnesota", "graduated", 9.85],
    ["Mississippi", "flat", 4.0],
    ["Missouri", "graduated", 4.7],
    ["Montana", "graduated", 5.65],
    ["Nebraska", "graduated", 4.55],
    ["Nevada", "none", 0],
    ["New Hampshire", "none", 0],
    ["New Jersey", "graduated", 10.75],
    ["New Mexico", "graduated", 5.9],
    ["New York", "graduated", 10.9],
    ["North Carolina", "flat", 3.99],
    ["North Dakota", "graduated", 2.5],
    ["Ohio", "flat", 2.75],
    ["Oklahoma", "graduated", 4.5],
    ["Oregon", "graduated", 9.9],
    ["Pennsylvania", "flat", 3.07],
    ["Rhode Island", "graduated", 5.99],
    ["South Carolina", "graduated", 5.21],
    ["South Dakota", "none", 0],
    ["Tennessee", "none", 0],
    ["Texas", "none", 0],
    ["Utah", "flat", 4.45],
    ["Vermont", "graduated", 8.75],
    ["Virginia", "graduated", 5.75],
    ["Washington", "none", 0],
    ["West Virginia", "graduated", 4.58],
    ["Wisconsin", "graduated", 7.65],
    ["Wyoming", "none", 0],
  ],

  // Full brackets for the graduated-tax states, single and married filing jointly (head of household is not shown).
  // Each row is [rate %, top of bracket]; the last row's top is null. A 0% first row is a zero bracket (income not taxed).
  // mfj: "same" means married filing jointly uses the single-filer brackets. Flat and no-tax states are not listed here.
  // Sources: Tax Foundation (Jan 1 / Apr 28, 2026) for most states; Arkansas (Act 2 of 2026), Maine (Maine Revenue Services),
  // South Carolina (SCDOR, H. 4216) and West Virginia (WV Tax Division, SB 392) from state sources because 2026 laws changed them.
  stateBrackets: {
    "Alabama": {
      single: [[2, 500], [4, 3000], [5, null]],
      mfj: [[2, 1000], [4, 6000], [5, null]],
    },
    "Arkansas": {
      single: [[0, 5599], [2, 11199], [3, 15999], [3.4, 26399], [3.7, null]],
      mfj: "same",
    },
    "California": {
      single: [[1, 11079], [2, 26264], [4, 41452], [6, 57542], [8, 72724], [9.3, 371479], [10.3, 445771], [11.3, 742953], [12.3, 1000000], [13.3, null]],
      mfj: [[1, 22158], [2, 52528], [4, 82904], [6, 115084], [8, 145448], [9.3, 742958], [10.3, 891542], [11.3, 1000000], [12.3, 1485906], [13.3, null]],
    },
    "Connecticut": {
      single: [[2, 10000], [4.5, 50000], [5.5, 100000], [6, 200000], [6.5, 250000], [6.9, 500000], [6.99, null]],
      mfj: [[2, 20000], [4.5, 100000], [5.5, 200000], [6, 400000], [6.5, 500000], [6.9, 1000000], [6.99, null]],
    },
    "Delaware": {
      single: [[0, 2000], [2.2, 5000], [3.9, 10000], [4.8, 20000], [5.2, 25000], [5.55, 60000], [6.6, null]],
      mfj: "same",
    },
    "District of Columbia": {
      single: [[4, 10000], [6, 40000], [6.5, 60000], [8.5, 250000], [9.25, 500000], [9.75, 1000000], [10.75, null]],
      mfj: "same",
    },
    "Hawaii": {
      single: [[1.4, 9600], [3.2, 14400], [5.5, 19200], [6.4, 24000], [6.8, 36000], [7.2, 48000], [7.6, 125000], [7.9, 175000], [8.25, 225000], [9, 275000], [10, 325000], [11, null]],
      mfj: [[1.4, 19200], [3.2, 28800], [5.5, 38400], [6.4, 48000], [6.8, 72000], [7.2, 96000], [7.6, 250000], [7.9, 350000], [8.25, 450000], [9, 550000], [10, 650000], [11, null]],
    },
    "Kansas": {
      single: [[5.2, 23000], [5.58, null]],
      mfj: [[5.2, 46000], [5.58, null]],
    },
    "Maine": {
      single: [[5.8, 27399], [6.75, 64849], [7.15, 1000000], [9.15, null]],
      mfj: [[5.8, 54849], [6.75, 129749], [7.15, 1500000], [9.15, null]],
    },
    "Maryland": {
      single: [[2, 1000], [3, 2000], [4, 3000], [4.75, 100000], [5, 125000], [5.25, 150000], [5.5, 250000], [5.75, 500000], [6.25, 1000000], [6.5, null]],
      mfj: [[2, 1000], [3, 2000], [4, 3000], [4.75, 150000], [5, 175000], [5.25, 225000], [5.5, 300000], [5.75, 600000], [6.25, 1200000], [6.5, null]],
    },
    "Massachusetts": {
      single: [[5, 1083150], [9, null]],
      mfj: "same",
    },
    "Minnesota": {
      single: [[5.35, 33310], [6.8, 109430], [7.85, 203150], [9.85, null]],
      mfj: [[5.35, 48700], [6.8, 193480], [7.85, 337930], [9.85, null]],
    },
    "Missouri": {
      single: [[0, 1348], [2, 2696], [2.5, 4044], [3, 5392], [3.5, 6740], [4, 8088], [4.5, 9436], [4.7, null]],
      mfj: "same",
    },
    "Montana": {
      single: [[4.7, 47500], [5.65, null]],
      mfj: [[4.7, 95000], [5.65, null]],
    },
    "Nebraska": {
      single: [[2.46, 4130], [3.51, 24760], [4.55, null]],
      mfj: [[2.46, 8250], [3.51, 49530], [4.55, null]],
    },
    "New Jersey": {
      single: [[1.4, 20000], [1.75, 35000], [3.5, 40000], [5.525, 75000], [6.37, 500000], [8.97, 1000000], [10.75, null]],
      mfj: [[1.4, 20000], [1.75, 50000], [2.45, 70000], [3.5, 80000], [5.525, 150000], [6.37, 500000], [8.97, 1000000], [10.75, null]],
    },
    "New Mexico": {
      single: [[1.5, 5500], [3.2, 16500], [4.3, 33500], [4.7, 66500], [4.9, 210000], [5.9, null]],
      mfj: [[1.5, 8000], [3.2, 25000], [4.3, 50000], [4.7, 100000], [4.9, 315000], [5.9, null]],
    },
    "New York": {
      single: [[3.9, 8500], [4.4, 11700], [5.15, 13900], [5.4, 80650], [5.9, 215400], [6.85, 1077550], [9.65, 5000000], [10.3, 25000000], [10.9, null]],
      mfj: [[3.9, 17150], [4.4, 23600], [5.15, 27900], [5.4, 161550], [5.9, 323200], [6.85, 2155350], [9.65, 5000000], [10.3, 25000000], [10.9, null]],
    },
    "North Dakota": {
      single: [[0, 48475], [1.95, 244825], [2.5, null]],
      mfj: [[0, 80975], [1.95, 298075], [2.5, null]],
    },
    "Oklahoma": {
      single: [[0, 3750], [2.5, 4900], [3.5, 7200], [4.5, null]],
      mfj: [[0, 7500], [2.5, 9800], [3.5, 14400], [4.5, null]],
    },
    "Oregon": {
      single: [[4.75, 4550], [6.75, 11400], [8.75, 125000], [9.9, null]],
      mfj: [[4.75, 9100], [6.75, 22800], [8.75, 250000], [9.9, null]],
    },
    "Rhode Island": {
      single: [[3.75, 82050], [4.75, 186450], [5.99, null]],
      mfj: "same",
    },
    "South Carolina": {
      single: [[1.99, 29999], [5.21, null]],
      mfj: "same",
    },
    "Vermont": {
      single: [[3.35, 49400], [6.6, 119700], [7.6, 249700], [8.75, null]],
      mfj: [[3.35, 82500], [6.6, 199450], [7.6, 304000], [8.75, null]],
    },
    "Virginia": {
      single: [[2, 3000], [3, 5000], [5, 17000], [5.75, null]],
      mfj: "same",
    },
    "West Virginia": {
      single: [[2.11, 10000], [2.81, 25000], [3.16, 40000], [4.22, 60000], [4.58, null]],
      mfj: "same",
    },
    "Wisconsin": {
      single: [[3.5, 15110], [4.4, 51950], [5.3, 332720], [7.65, null]],
      mfj: [[3.5, 20150], [4.4, 69260], [5.3, 443630], [7.65, null]],
    },
  },

  stateNotes: {
    "Arkansas": "Brackets shown are for taxable income of $94,700 or less. Above that, a separate two-rate table applies: 2% on the first $4,700 and 3.7% on the rest. The 3.7% top rate took effect for 2026 under a law signed in May.",
    "California": "The top rate includes the 1% mental health services tax on income over $1 million. Bracket amounts are the 2025 inflation-adjusted figures.",
    "Connecticut": "Phase-outs and benefit recapture mean many higher-income filers pay more than the brackets alone suggest.",
    "Idaho": "The 5.3% rate applies to taxable income above $4,811 (single) or $9,622 (married filing jointly). Bracket amounts are the 2025 figures.",
    "Maine": "Includes a 2% surtax on income above $1 million (single) or $1.5 million (joint), enacted in 2026 and retroactive to January 1.",
    "Massachusetts": "The 9% bracket is the 5% rate plus a 4% surtax on income above $1,083,150. Bracket amounts are the 2025 figures.",
    "Mississippi": "The 4% rate applies to taxable income above $10,000; the first $10,000 is not taxed.",
    "New Hampshire": "No tax on wages. The tax on interest and dividends was repealed starting in 2025.",
    "New York": "Many high-income filers pay their top rate on all income, not just the amount above the bracket threshold (tax benefit recapture).",
    "North Dakota": "Bracket amounts are the 2025 inflation-adjusted figures.",
    "Ohio": "No tax on the first $26,050 of income, then a flat 2.75%.",
    "South Carolina": "Restructured for 2026 (H. 4216): 1.99% up to $30,000 and 5.21% above, the same for every filing status. The old 0%, 3% and 6% schedule no longer applies.",
    "Vermont": "Bracket amounts are the 2025 inflation-adjusted figures.",
    "Washington": "No tax on wages. A separate excise tax applies to large long-term capital gains.",
  },
};
