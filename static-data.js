/*
  Figures that change once a year. Update this file each fall when the IRS
  publishes the next year's inflation adjustments (usually October/November),
  and in January for state rate changes. When you change figures, also update
  the matching "Data as of" label in the asOf block below.

  Sources
    Federal brackets, standard deduction: IRS Rev. Proc. 2025-32 (tax year 2026)
    Retirement/HSA limits: IRS Notice 2025-67 and Rev. Proc. 2025-19 (tax year 2026)
    State rates: Tax Foundation, rates as of January 1, 2026
*/
window.STATIC = {
  taxYear: 2026,

  // "Data as of" labels shown under each hand-entered table on the page.
  // Change these whenever you update the figures below them.
  asOf: {
    brackets: { date: "Tax year 2026", source: "IRS Rev. Proc. 2025-32" },
    limits: { date: "Tax year 2026", source: "IRS Notice 2025-67 and Rev. Proc. 2025-19" },
    states: { date: "January 1, 2026", source: "Tax Foundation" },
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
    ["Arkansas", "graduated", 3.9],
    ["California", "graduated", 13.3],
    ["Colorado", "flat", 4.4],
    ["Connecticut", "graduated", 6.99],
    ["Delaware", "graduated", 6.6],
    ["District of Columbia", "graduated", 10.75],
    ["Florida", "none", 0],
    ["Georgia", "flat", 5.19],
    ["Hawaii", "graduated", 11.0],
    ["Idaho", "flat", 5.3],
    ["Illinois", "flat", 4.95],
    ["Indiana", "flat", 2.95],
    ["Iowa", "flat", 3.8],
    ["Kansas", "graduated", 5.58],
    ["Kentucky", "flat", 3.5],
    ["Louisiana", "flat", 3.0],
    ["Maine", "graduated", 7.15],
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
    ["Ohio", "graduated", 2.75],
    ["Oklahoma", "graduated", 4.5],
    ["Oregon", "graduated", 9.9],
    ["Pennsylvania", "flat", 3.07],
    ["Rhode Island", "graduated", 5.99],
    ["South Carolina", "graduated", 6.0],
    ["South Dakota", "none", 0],
    ["Tennessee", "none", 0],
    ["Texas", "none", 0],
    ["Utah", "flat", 4.5],
    ["Vermont", "graduated", 8.75],
    ["Virginia", "graduated", 5.75],
    ["Washington", "none", 0],
    ["West Virginia", "graduated", 4.82],
    ["Wisconsin", "graduated", 7.65],
    ["Wyoming", "none", 0],
  ],

  stateNotes: {
    "Massachusetts": "5% on most income, plus a 4% surtax on income above about $1 million.",
    "Washington": "No tax on wages. A separate excise tax applies to large long-term capital gains.",
    "New Hampshire": "No tax on wages. The tax on interest and dividends was repealed starting in 2025.",
    "Ohio": "No tax on the first $26,050 of income, then a flat 2.75%.",
  },
};
