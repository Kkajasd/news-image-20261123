#!/usr/bin/env python3
"""Draw the 1024x1024 front page for news-image-20261123.

"The World Today" front page summing up Monday 23 November 2026:
Nvidia reinstates Jensen Huang as the lead, 18 more stories in a 3x6
grid, and 8 items in brief. Deterministic: fixed text, fixed colours,
fixed geometry, no timestamps, no randomness. Output: entry.png in the
repository root, next to main.ts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (17, 17, 17)
RED = (166, 25, 46)
GREEN = (18, 110, 60)
GREY = (85, 85, 85)
LIGHT_GREY = (180, 175, 165)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "NotoSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_illustration(draw, x0, y0, x1, y1):
    """Flat-colour panel: a green microchip with circuit pins and a
    steep rising market line. No text inside the panel."""
    # Dark board background
    draw.rectangle([x0, y0, x1, y1], fill=(24, 48, 38))
    # Faint grid dots
    for gy in range(y0 + 14, y1 - 8, 18):
        for gx in range(x0 + 14, x1 - 8, 18):
            draw.rectangle([gx, gy, gx + 2, gy + 2], fill=(52, 96, 74))
    # Rising market line (white, thick)
    pts = [(x0 + 12, y1 - 34), (x0 + 70, y1 - 62), (x0 + 120, y1 - 52),
           (x0 + 175, y1 - 96), (x0 + 225, y1 - 84), (x0 + 285, y1 - 138)]
    draw.line(pts, fill=(255, 255, 255), width=5, joint="curve")
    # Arrowhead at the end of the line
    ex, ey = pts[-1]
    draw.polygon([(ex - 2, ey - 16), (ex + 16, ey + 2), (ex - 14, ey + 6)],
                 fill=(255, 255, 255))
    # Microchip in the lower left
    cx0, cy0, cx1, cy1 = x0 + 22, y1 - 74, x0 + 118, y1 - 10
    # Pins
    for i in range(4):
        px = cx0 + 12 + i * 24
        draw.rectangle([px, cy0 - 10, px + 5, cy0], fill=(214, 196, 120))
        draw.rectangle([px, cy1, px + 5, cy1 + 10], fill=(214, 196, 120))
        py = cy0 + 10 + i * 14
        draw.rectangle([cx0 - 10, py, cx0, py + 5], fill=(214, 196, 120))
        draw.rectangle([cx1, py, cx1 + 10, py + 5], fill=(214, 196, 120))
    draw.rectangle([cx0, cy0, cx1, cy1], fill=(18, 110, 60))
    draw.rectangle([cx0, cy0, cx1, cy1], outline=(214, 196, 120), width=2)
    # Inner die
    draw.rectangle([cx0 + 26, cy0 + 16, cx1 - 26, cy1 - 16],
                   fill=(24, 48, 38))
    draw.rectangle([cx0 + 32, cy0 + 22, cx1 - 32, cy1 - 22],
                   outline=(120, 200, 150), width=1)
    # Frame
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


STORIES = [
    ("MARKETS", "Wall Street roars back on Nvidia",
     "The S&P 500 rose 4.7% and the Nasdaq 6.5% as Nvidia's return reignited the AI trade after last week's rout."),
    ("MARKETS", "Kospi falls 3.3% as AI rout hits Asia",
     "Seoul's Kospi closed 3.31% lower, its lowest in 10 months, and the government readied a $6.8bn stabilisation fund."),
    ("AI", "Guterres calls for global AI safety rules",
     "At the Bridgetown summit, the UN chief warned AI is driving 'the biggest transfer of power in human history'."),
    ("UK", "Burnham hails EU reset deal to MPs",
     "The PM told Parliament the landmark deal could make the next decade 'much better', claiming a GBP 17bn boost."),
    ("MEXICO", "Death toll in 'El Chapo Isidro' raid rises to 20",
     "Sixteen gunmen and four soldiers died in the Sinaloa raid; the US seeks the cartel boss's extradition."),
    ("IRAN", "IDF warns Netanyahu: Iran strike could widen war",
     "Israel's military warned a strike on Iran could trigger a wider regional conflict, as Netanyahu presses Trump to act."),
    ("KOREA", "Minister quits over AI exam-cheating chaos",
     "Education minister Choi Kyo-jin resigned after last-minute anti-cheating rules confused exam candidates."),
    ("EU", "EU Academy data leaked in AI cyberattack",
     "The Commission confirmed names and emails of users were exposed; the platform went offline."),
    ("RUSSIA", "700,000 Russian soldiers dead, study finds",
     "Meduza and Mediazona estimate the toll from leaked Rosstat records; 490,000 deaths registered."),
    ("AUSTRALIA", "Molly Meldrum dies aged 83",
     "The Countdown host who championed AC/DC and Kylie Minogue died in Melbourne; a state funeral follows."),
    ("LIBYA", "UN urges probe into Benghazi port attacks",
     "The UN mission called for an investigation after drone strikes hit Russian ships at the Libyan port."),
    ("GAZA", "Second wave of Gaza children reach UK for NHS care",
     "Critically ill children were evacuated for specialist treatment, the British government said."),
    ("CLIMATE", "COP31 fallout: Pacific nations despair",
     "Blame began for the collapsed talks, with Australia's opposition calling for the minister who led them to resign."),
    ("SPAIN", "Spain's right tipped for majority",
     "Final polls before Sunday's vote put the PP and Vox above the 176-seat majority line in the 350-seat house."),
    ("BANGLADESH", "Dhaka: Hasina will be arrested if she returns",
     "Bangladesh said it will jail the former prime minister if she comes back from exile."),
    ("SPORT", "Brentford thrash 10-man Everton 4-0",
     "Lewis-Potter scored twice in two minutes and Janelt hit a 30-yard stunner as Brentford climbed to sixth."),
    ("CONGO", "WHO counts 87 attacks on Congo health care",
     "The WHO has verified more than 87 attacks on health care in DR Congo this year amid the Ebola response."),
    ("CYBER", "Reports: EU suspects China-linked hackers",
     "The Commission is reported to suspect a China-backed group, codenamed 'Panda', behind the attack."),
]

IN_BRIEF_LEFT = [
    "Kushner links Ukraine guarantees to Article 5",
    "Murmansk governor held over suspected funds misuse",
    "Bessent: US seeks answers on Nvidia chip sales to China",
    "Thailand draws up list of mining chemicals to ban",
]
IN_BRIEF_RIGHT = [
    "Erdogan: COP31 laid foundations despite no deal",
    "Macron pushes budget rule to bind future leaders",
    "Iran president switches off office lights to save power",
    "Saudi Arabia condemns attack on UN building in Khartoum",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 26                      # left margin
    right = W - 26               # right edge of content
    content_w = right - mx       # 972

    # ---- Top thin rule ----
    draw.rectangle([mx, 8, right, 10], fill=RULE)

    # ---- Masthead ----
    f_mast = font(SERIF_B, 70)
    mast = "The World Today"
    mw = draw.textlength(mast, font=f_mast)
    draw.text(((W - mw) / 2, 14), mast, font=f_mast, fill=INK)

    # ---- Dateline (large, unmistakable) ----
    f_date = font(SANS_B, 26)
    date = "Monday, 23 November 2026"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, 96), date, font=f_date, fill=RED)
    f_date_small = font(SANS, 12)
    small = "WORLD EDITION  |  No. 328  |  ALL THE NEWS OF THE DAY"
    sw = draw.textlength(small, font=f_date_small)
    draw.text(((W - sw) / 2, 128), small, font=f_date_small, fill=GREY)

    # ---- Red rule ----
    draw.rectangle([mx, 150, right, 154], fill=RED)

    # ---- Markets ticker ----
    f_tick = font(SANS, 13)
    tick = "S&P 500  +4.7%      Nasdaq  +6.5%      Dow  +1,448      Kospi  -3.3%      Nvidia  +31%      Bitcoin  $61,000"
    tw = draw.textlength(tick, font=f_tick)
    draw.text(((W - tw) / 2, 160), tick, font=f_tick, fill=INK)
    draw.rectangle([mx, 182, right, 183], fill=LIGHT_GREY)

    # ---- Lead story ----
    lead_x = mx
    lead_w = 626
    ill_x0, ill_y0 = 668, 192
    ill_x1, ill_y1 = right, 360
    f_kick = font(SANS_B, 12)
    draw.text((lead_x, 192), "TECH  -  NVIDIA'S COMEBACK", font=f_kick, fill=RED)
    f_lead_h = font(SERIF_B, 32)
    lead_head = "Huang is back: Nvidia reinstates its CEO"
    lh_lines = wrap(draw, lead_head, f_lead_h, lead_w)
    y = draw_lines(draw, lead_x, 214, lh_lines, f_lead_h, INK, 38)
    f_lead_b = font(SERIF, 14)
    lead_body = ("Nvidia's board unanimously reinstated Jensen Huang as president "
                 "and chief executive, 11 days after he resigned over a scandal "
                 "involving extramarital affairs, one with a woman US officials "
                 "suspect of spying for China. Shares jumped 31%, their best day "
                 "since 2003, adding about $950bn in value, as Wall Street roared back.")
    lb_lines = wrap(draw, lead_body, f_lead_b, lead_w)
    y = draw_lines(draw, lead_x, y + 8, lb_lines, f_lead_b, INK, 18)
    f_by = font(SERIF_I, 12)
    draw.text((lead_x, y + 8), "By The World Today staff  -  Santa Clara, California",
              font=f_by, fill=GREY)

    # Illustration panel (right of lead)
    draw_illustration(draw, ill_x0, ill_y0, ill_x1, ill_y1)
    f_cap = font(SERIF_I, 11)
    cap = "Nvidia shares jumped 31% on the day, their best since 2003."
    cap_lines = wrap(draw, cap, f_cap, ill_x1 - ill_x0)
    draw_lines(draw, ill_x0, ill_y1 + 6, cap_lines, f_cap, GREY, 14)

    # ---- Rule above story grid ----
    draw.rectangle([mx, 404, right, 406], fill=RULE)

    # ---- Story grid: 3 columns x 6 stories ----
    f_label = font(SANS_B, 10)
    f_head = font(SERIF_B, 16)
    f_body = font(SERIF, 11)
    col_gap = 14
    col_w = (content_w - 2 * col_gap) // 3   # 314
    col_xs = [mx, mx + col_w + col_gap, mx + 2 * (col_w + col_gap)]
    grid_top = 418
    grid_bottom = 912
    columns = [STORIES[0:6], STORIES[6:12], STORIES[12:18]]
    for ci, col in enumerate(columns):
        x = col_xs[ci]
        y = grid_top
        for label, headline, body in col:
            draw.text((x, y), label, font=f_label, fill=RED)
            y += 11
            h_lines = wrap(draw, headline, f_head, col_w)
            if len(h_lines) > 2:
                h_lines = h_lines[:2]
                h_lines[-1] = h_lines[-1].rstrip() + " ..."
            y = draw_lines(draw, x, y, h_lines, f_head, INK, 18)
            b_lines = wrap(draw, body, f_body, col_w)
            if len(b_lines) > 2:
                b_lines = b_lines[:2]
                b_lines[-1] = b_lines[-1].rstrip() + " ..."
            y = draw_lines(draw, x, y + 1, b_lines, f_body, INK, 13)
            y += 3
            if (label, headline, body) is not col[-1]:
                draw.rectangle([x, y, x + col_w, y], fill=LIGHT_GREY)
                y += 4
        if y > grid_bottom + 2:
            raise SystemExit("column %d overflows grid: bottom y=%d > %d"
                             % (ci, y, grid_bottom))
        if ci < 2:
            vx = x + col_w + col_gap // 2
            draw.line([vx, grid_top, vx, grid_bottom], fill=LIGHT_GREY, width=1)

    # ---- Rule above In Brief ----
    draw.rectangle([mx, 920, right, 922], fill=RULE)

    # ---- In Brief strip (two columns) ----
    f_ib_h = font(SANS_B, 13)
    draw.text((mx, 930), "IN BRIEF", font=f_ib_h, fill=RED)
    f_ib = font(SANS, 12)
    ib_y = 950
    mid = mx + content_w // 2 + 8
    for item in IN_BRIEF_LEFT:
        draw.text((mx, ib_y), "-  " + item, font=f_ib, fill=INK)
        ib_y += 14
    ib_y = 950
    for item in IN_BRIEF_RIGHT:
        draw.text((mid, ib_y), "-  " + item, font=f_ib, fill=INK)
        ib_y += 14

    # ---- Footer ----
    f_foot = font(SANS, 10)
    foot = "The World Today  -  Monday 23 November 2026"
    fw = draw.textlength(foot, font=f_foot)
    draw.text(((W - fw) / 2, 1010), foot, font=f_foot, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote %s %dx%d" % (OUT, W, H))


if __name__ == "__main__":
    main()
