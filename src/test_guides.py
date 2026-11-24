"""
test_guides.py: measuring instructions and slider settings for the app.
"""

PHYSICAL_TESTS = [{'key': 'sprint_time',
  'label': '30m Sprint Time (seconds)',
  'min': 3.5,
  'max': 6.0,
  'default': 4.2,
  'step': 0.1,
  'guide_title': '❓ How do I time my 30m sprint?',
  'guide_md': '**Setup:** mark a straight, flat 30m stretch with two cones (start and finish). '
              'Warm up first with light jogging and a few practice accelerations.\n'
              '\n'
              '**How to run it:** start from a stationary position, sprint maximally through the '
              "finish cone (don't slow down before it), and have a partner time you with a "
              'stopwatch from your first movement to when you cross the line. Run it twice and '
              'record your best time.\n'
              '\n'
              '[Full protocol — Topend '
              'Sports](https://www.topendsports.com/testing/tests/sprint-30meters.htm)'},
 {'key': 'shuttle_time',
  'label': '5-10-5 Shuttle Time (seconds)',
  'min': 4.0,
  'max': 7.0,
  'default': 4.8,
  'step': 0.1,
  'guide_title': '❓ How do I run the 5-10-5 shuttle?',
  'guide_md': '**Setup:** place 3 cones in a straight line, 5 yards apart (so 10 yards total '
              'between the outer two).\n'
              '\n'
              '**How to run it:** start straddling the middle cone in a 3-point stance. Sprint 5 '
              'yards to one side and touch the line, change direction and sprint 10 yards to the '
              'far cone and touch it, then sprint back 5 yards through the middle cone to finish. '
              'Time starts on your first movement and stops when you cross the middle cone at the '
              'end.\n'
              '\n'
              '[Full protocol — Science for '
              'Sport](https://www.scienceforsport.com/pro-agility-5-10-5-test/) · [Video '
              'walkthrough](https://www.youtube.com/watch?v=tYhCJd7LaBU)'},
 {'key': 'bench_reps',
  'label': 'Max Bench Press Reps (135 lbs)',
  'min': 0,
  'max': 30,
  'default': 12,
  'step': None,
  'guide_title': '❓ How do I test max bench press reps?',
  'guide_md': '**Setup:** standard barbell + 135 lbs loaded, bench with a spotter present. '
              '**Always use a spotter for this test.**\n'
              '\n'
              '**How to run it:** lie flat, grip the bar shoulder-width apart, lower it to your '
              "chest with control, then press to full elbow extension. That's 1 rep. Repeat with "
              "proper form until you can't complete another full rep — that count is your score.\n"
              '\n'
              '[Full protocol — Topend '
              'Sports](https://www.topendsports.com/testing/tests/max-bench-press.htm)'}]

TECHNICAL_TESTS = {'Forward': [{'key': 'finishing',
              'label': 'Finishing (Shot Accuracy)',
              'min': 30,
              'max': 99,
              'default': 68,
              'step': None,
              'guide_title': '❓ How do I rate my Finishing (Shot Accuracy)?',
              'guide_md': '**Objective anchor:** take 10 shots at a goal (or a target on a wall) '
                          'from 12-18 yards, varying angle and pace of service. Count how many go '
                          "exactly where you intended, not just 'on target.'\n"
                          '\n'
                          '- **2-3/10 on target, poor placement control** → rate **30-45**\n'
                          '- **4-6/10, decent placement but inconsistent under pressure** → rate '
                          '**45-65**\n'
                          '- **7-8/10, reliable placement, both feet usable** → rate **65-80**\n'
                          '- **9-10/10 consistently, clinical under pressure/1st touch finishes** '
                          '→ rate **80+**'},
             {'key': 'shotpower',
              'label': 'Shot Power',
              'min': 30,
              'max': 99,
              'default': 68,
              'step': None,
              'guide_title': '❓ How do I rate my Shot Power?',
              'guide_md': '**Objective anchor — ball speed.** If you have access to a radar/speed '
                          'gun app, real-world shot speeds break down roughly like this:\n'
                          '\n'
                          '- **Youth/U12: ~30-40 mph** → rate **30-45**\n'
                          '- **Amateur/recreational adult: ~40-55 mph** → rate **45-60**\n'
                          '- **Competitive club/high school: ~55-65 mph** → rate **60-70**\n'
                          '- **Strong amateur/college level: ~65-70 mph** → rate **70-80**\n'
                          '- **Professional average: ~70-80 mph** → rate **80-90**\n'
                          '- **Elite pro / top strikers: 80mph+** → rate **90+**\n'
                          '\n'
                          "**No radar gun?** Rate how hard you're able to strike it while still "
                          'keeping the shot on target — raw power that sends the ball wildly off '
                          "target isn't useful power.\n"
                          '\n'
                          '[Shot speed '
                          'research](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2026.1766063/full) '
                          '· [Pro vs. amateur '
                          'benchmarks](https://stmichaelssoccer.com/rules-rocketing-shots-how-fast-are-soccer-shots/)'},
             {'key': 'dribbling',
              'label': 'Dribbling',
              'min': 30,
              'max': 99,
              'default': 68,
              'step': None,
              'guide_title': '❓ How do I rate my Dribbling?',
              'guide_md': '**Objective anchor — cone weave drill.** Set up 5-6 cones 5 yards '
                          'apart, weave through with both feet, staying tight.\n'
                          '\n'
                          '- **12-15+ sec, frequent loss of control** → rate **30-45**\n'
                          '- **8-10 sec, occasional wide touches** → rate **45-60**\n'
                          '- **Under 8 sec, tight touches, comfortable both feet** → rate '
                          '**60-75**\n'
                          '- **Fast, tight, beats real defenders 1v1 in games** → rate **75-90**\n'
                          '\n'
                          '[Cone drill '
                          'benchmarks](https://goalnyx.com/soccer-cone-drills-for-ball-control/)'},
             {'key': 'longshots',
              'label': 'Long Shots',
              'min': 30,
              'max': 99,
              'default': 60,
              'step': None,
              'guide_title': '❓ How do I rate my Long Shots?',
              'guide_md': '**Objective anchor:** take 10 shots from 25+ yards at a goal or wall '
                          'target. Count how many stay on target (not just how many would be '
                          'goals).\n'
                          '\n'
                          '- **0-2/10 on target** → rate **30-45**\n'
                          '- **3-5/10 on target** → rate **45-65**\n'
                          '- **6-8/10 on target, decent placement from distance** → rate '
                          '**65-80**\n'
                          '- **9-10/10, genuine threat from distance** → rate **80+**'},
             {'key': 'positioning',
              'label': 'Positioning',
              'min': 30,
              'max': 99,
              'default': 65,
              'step': None,
              'guide_title': '❓ How do I rate my Positioning?',
              'guide_md': "Positioning is about *where you are before the ball arrives*, so it's "
                          'hard to time-test — use this checklist from your last few games '
                          'instead:\n'
                          '\n'
                          '- I regularly get goal-scoring chances without needing to dribble past '
                          'multiple defenders first\n'
                          '- I time my runs to beat the offside line rather than getting caught '
                          'level or behind\n'
                          '- Coaches/teammates say I find space well in the box\n'
                          '- I get more shots per game than most attacking teammates\n'
                          '- I react quickly to loose balls/rebounds in the box\n'
                          '\n'
                          '**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · **4-5 '
                          'true, consistently** → rate **70-90**'},
             {'key': 'headingaccuracy',
              'label': 'Heading Accuracy',
              'min': 30,
              'max': 99,
              'default': 60,
              'step': None,
              'guide_title': '❓ How do I rate my Heading Accuracy?',
              'guide_md': '**Objective anchor — aerial duel win rate.** Over a few games or '
                          'crossing/heading drills, track contested headers won vs. attempted.\n'
                          '\n'
                          '- **Under 40% win rate** → rate **30-50**\n'
                          '- **40-55% win rate** → rate **50-65**\n'
                          '- **55-70% win rate** → rate **65-80**\n'
                          '- **70%+ win rate (above pro top-flight average of ~66%)** → rate '
                          '**80+**\n'
                          '\n'
                          '[Aerial duel '
                          'benchmarks](https://www.athletepath.com/soccer-aerial-duel-calculator/)'},
             {'key': 'curve',
              'label': 'Curve',
              'min': 30,
              'max': 99,
              'default': 55,
              'step': None,
              'guide_title': '❓ How do I rate my Curve?',
              'guide_md': '**Objective anchor:** from the corner of the 18-yard box, try to bend '
                          '10 shots around an obstacle (a cone or bag placed between you and the '
                          'goal) and on target.\n'
                          '\n'
                          '- **0-2/10 successfully bent on target** → rate **30-50**\n'
                          '- **3-5/10** → rate **50-65**\n'
                          '- **6-8/10, reliable curl on both power and placed shots** → rate '
                          '**65-80**\n'
                          '- **9-10/10, can consistently shape shots around a wall/defender** → '
                          'rate **80+**'},
             {'key': 'penalties',
              'label': 'Penalties',
              'min': 30,
              'max': 99,
              'default': 60,
              'step': None,
              'guide_title': '❓ How do I rate my Penalties?',
              'guide_md': '**Objective anchor — conversion rate.** Track your last 10 penalty '
                          'attempts (practice counts, but game penalties are more representative '
                          'since nerves are part of the skill).\n'
                          '\n'
                          '- **Under 50% scored** → rate **30-50**\n'
                          '- **50-65% scored** → rate **50-65**\n'
                          '- **65-80% scored (near pro average of ~76-85% in regular play)** → '
                          'rate **65-85**\n'
                          '- **85%+ scored, consistently composed** → rate **85+**\n'
                          '\n'
                          '[Pro penalty conversion '
                          'data](https://www.athletepath.com/soccer-penalty-conversion-calculator/)'},
             {'key': 'crossing',
              'label': 'Crossing',
              'min': 30,
              'max': 99,
              'default': 55,
              'step': None,
              'guide_title': '❓ How do I rate my Crossing?',
              'guide_md': 'Mainly relevant if you play wide. **Objective anchor:** deliver 10 '
                          'crosses from the flank into the box aimed at a target (cone, teammate, '
                          'or marked zone).\n'
                          '\n'
                          '- **0-2/10 reach the target zone** → rate **30-50**\n'
                          '- **3-5/10** → rate **50-65**\n'
                          '- **6-8/10, consistent delivery, good pace on the ball** → rate '
                          '**65-80**\n'
                          '- **9-10/10, reliably picks out a specific target** → rate **80+**'}],
 'Midfielder': [{'key': 'passing',
                 'label': 'Short Passing Accuracy',
                 'min': 30,
                 'max': 99,
                 'default': 72,
                 'step': None,
                 'guide_title': '❓ How do I rate my Passing Accuracy?',
                 'guide_md': '**Objective anchor — wall pass test.** Stand 5-8 yards from a flat '
                             'wall, pass with the inside of your foot, control the rebound with '
                             'one touch, pass again. Do 100 total attempts (50 per foot), count '
                             'clean/accurate returns.\n'
                             '\n'
                             '- **Under 50/100 clean** → rate **30-45**\n'
                             '- **50-70/100 clean** → rate **45-60**\n'
                             '- **70-85/100 clean** → rate **60-75**\n'
                             '- **85-95/100 clean, solid weak foot too** → rate **75-88**\n'
                             '- **95+/100 clean, minimal foot difference** → rate **88+**\n'
                             '\n'
                             '**Context:** professional teams complete roughly **77-82%** of all '
                             'passes in matches (with defensive pressure), and **90-95%** on '
                             'simple ground passes. Since a wall drill has no defender, aim well '
                             'above match-pressure rates to justify a top-tier score.\n'
                             '\n'
                             '[Wall pass '
                             'benchmarks](https://www.ritfitsports.com/blogs/article/how-to-improve-soccer-passing) '
                             '· [Pro passing accuracy '
                             'data](https://www.sportmonks.com/glossary/passing-accuracy/)'},
                {'key': 'ballcontrol',
                 'label': 'Ball Control',
                 'min': 30,
                 'max': 99,
                 'default': 70,
                 'step': None,
                 'guide_title': '❓ How do I rate my Ball Control?',
                 'guide_md': '**Objective anchor — cone weave / juggling.** Weave a ball through '
                             '5-6 cones 5 yards apart using both feet, staying tight, OR count how '
                             'many consecutive juggles you can do without the ball hitting the '
                             'ground.\n'
                             '\n'
                             '- **10+ seconds through cones / under 10 juggles** → rate **30-45**\n'
                             '- **8-10 sec / 10-20 juggles** → rate **45-60**\n'
                             '- **Under 8 sec, tight touches / 20-50 juggles** → rate **60-75**\n'
                             '- **Fast + tight, comfortable both feet / 50+ juggles** → rate '
                             '**75-90**\n'
                             '\n'
                             '[Cone drill '
                             'benchmarks](https://goalnyx.com/soccer-cone-drills-for-ball-control/)'},
                {'key': 'vision',
                 'label': 'Vision',
                 'min': 30,
                 'max': 99,
                 'default': 70,
                 'step': None,
                 'guide_title': '❓ How do I rate my Vision?',
                 'guide_md': 'Vision is harder to self-time, so use this self-assessment checklist '
                             'instead — count how many describe you honestly:\n'
                             '\n'
                             '- I scan over my shoulder *before* receiving the ball, not after\n'
                             '- I regularly spot a teammate in space that others miss\n'
                             "- I can complete a first-time pass into a teammate's stride without "
                             'looking twice\n'
                             '- Coaches/teammates have specifically praised my passing choices, '
                             'not just my technique\n'
                             '- I rarely give the ball away because I passed into a bad situation\n'
                             '\n'
                             '**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · **4 '
                             'true** → rate **70-85** · **5 true, consistently** → rate **85+**\n'
                             '\n'
                             '[Scanning & passing vision '
                             'research](https://www.mdpi.com/2673-7078/5/3/61)'},
                {'key': 'dribbling',
                 'label': 'Dribbling',
                 'min': 30,
                 'max': 99,
                 'default': 65,
                 'step': None,
                 'guide_title': '❓ How do I rate my Dribbling?',
                 'guide_md': '**Objective anchor — cone weave drill.** Set up 5-6 cones 5 yards '
                             'apart, weave through with both feet, staying tight under simulated '
                             'pressure.\n'
                             '\n'
                             '- **12-15+ sec, frequent loss of control** → rate **30-45**\n'
                             '- **8-10 sec, occasional wide touches** → rate **45-60**\n'
                             '- **Under 8 sec, tight touches, comfortable both feet** → rate '
                             '**60-75**\n'
                             '- **Fast, tight, retains possession under real pressure in games** → '
                             'rate **75-90**\n'
                             '\n'
                             '[Cone drill '
                             'benchmarks](https://goalnyx.com/soccer-cone-drills-for-ball-control/)'},
                {'key': 'crossing',
                 'label': 'Crossing',
                 'min': 30,
                 'max': 99,
                 'default': 55,
                 'step': None,
                 'guide_title': '❓ How do I rate my Crossing?',
                 'guide_md': '**Objective anchor:** deliver 10 crosses/switches of play into the '
                             'box or to a target zone from a wide or deep position.\n'
                             '\n'
                             '- **0-2/10 reach the target zone** → rate **30-50**\n'
                             '- **3-5/10** → rate **50-65**\n'
                             '- **6-8/10, consistent delivery** → rate **65-80**\n'
                             '- **9-10/10, reliably picks out a specific target** → rate **80+**'},
                {'key': 'curve',
                 'label': 'Curve',
                 'min': 30,
                 'max': 99,
                 'default': 55,
                 'step': None,
                 'guide_title': '❓ How do I rate my Curve?',
                 'guide_md': '**Objective anchor:** try to bend 10 long passes or shots around an '
                             'obstacle placed between you and the target, landing on target.\n'
                             '\n'
                             '- **0-2/10 successfully bent on target** → rate **30-50**\n'
                             '- **3-5/10** → rate **50-65**\n'
                             '- **6-8/10, reliable curl on passes/shots** → rate **65-80**\n'
                             '- **9-10/10, can consistently shape the ball around obstacles** → '
                             'rate **80+**'},
                {'key': 'freekickaccuracy',
                 'label': 'Free Kick Accuracy',
                 'min': 30,
                 'max': 99,
                 'default': 55,
                 'step': None,
                 'guide_title': '❓ How do I rate my Free Kick Accuracy?',
                 'guide_md': '**Objective anchor:** take 10 direct free kicks from 18-25 yards at '
                             'a goal (use a wall of cones/bags to simulate a defensive wall if '
                             'possible).\n'
                             '\n'
                             '- **0-2/10 on target** → rate **30-50**\n'
                             '- **3-5/10** → rate **50-65**\n'
                             '- **6-8/10, consistent placement over/around a wall** → rate '
                             '**65-80**\n'
                             '- **9-10/10, genuine set-piece threat** → rate **80+**'},
                {'key': 'composure',
                 'label': 'Composure',
                 'min': 30,
                 'max': 99,
                 'default': 65,
                 'step': None,
                 'guide_title': '❓ How do I rate my Composure?',
                 'guide_md': 'Composure is decision-making quality under pressure — use this '
                             'checklist honestly based on recent real games:\n'
                             '\n'
                             '- I take my first touch calmly even when closed down immediately\n'
                             '- I rarely panic-clear or panic-pass under pressure\n'
                             '- I can slow the game down when needed instead of always rushing\n'
                             "- My decision quality doesn't drop late in games when tired\n"
                             '- I stay level-headed after a mistake instead of it affecting my '
                             'next few plays\n'
                             '\n'
                             '**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · '
                             '**4-5 true, consistently** → rate **70-90**'},
                {'key': 'stamina',
                 'label': 'Stamina',
                 'min': 30,
                 'max': 99,
                 'default': 65,
                 'step': None,
                 'guide_title': '❓ How do I rate my Stamina?',
                 'guide_md': '**Objective anchor — beep test (multi-stage fitness test).** Run the '
                             'standard 20m shuttle beep test and note the level you reach before '
                             'you can no longer keep pace.\n'
                             '\n'
                             '- **Level 6-8** → rate **30-50**\n'
                             '- **Level 9-10 (solid recreational/amateur fitness)** → rate '
                             '**50-65**\n'
                             '- **Level 11-13 (strong amateur/college level)** → rate **65-80**\n'
                             '- **Level 14+ (elite outfield range; pro midfielders often score '
                             'highest of any position)** → rate **80+**\n'
                             '\n'
                             '[Beep test standards by '
                             'level](https://peakvo2trainer.com/blog/beep-test-soccer/) · '
                             '[Age/position '
                             'benchmarks](https://www.thebeeptest.com/sports/football)'},
                {'key': 'longshots',
                 'label': 'Long Shots',
                 'min': 30,
                 'max': 99,
                 'default': 55,
                 'step': None,
                 'guide_title': '❓ How do I rate my Long Shots?',
                 'guide_md': '**Objective anchor:** take 10 shots from 25+ yards at a goal or wall '
                             'target, counting how many stay on target.\n'
                             '\n'
                             '- **0-2/10 on target** → rate **30-45**\n'
                             '- **3-5/10 on target** → rate **45-65**\n'
                             '- **6-8/10 on target** → rate **65-80**\n'
                             '- **9-10/10, genuine threat from distance** → rate **80+**'}],
 'Defender': [{'key': 'standingtackle',
               'label': 'Standing Tackle',
               'min': 30,
               'max': 99,
               'default': 70,
               'step': None,
               'guide_title': '❓ How do I rate my Standing Tackle?',
               'guide_md': '**Objective anchor — tackle success rate.** Over your next few '
                           'practice games or 1v1 defending drills, track: attempted standing '
                           'tackles vs. tackles won cleanly (no foul, ball recovered).\n'
                           '\n'
                           '- **Under 40% win rate** → rate **30-50**\n'
                           '- **40-55% win rate** → rate **50-65**\n'
                           '- **55-70% win rate** → rate **65-80**\n'
                           '- **70%+ win rate (matches pro top-flight average)** → rate **80+**\n'
                           '\n'
                           'Pros in top leagues average roughly **60-65% tackle success**, with '
                           '**70%+ considered excellent** — use that as your ceiling reference, '
                           'not your floor.\n'
                           '\n'
                           '[Tackle success '
                           'benchmarks](https://www.athletepath.com/soccer-tackle-success-rate-calculator/)'},
              {'key': 'slidingtackle',
               'label': 'Sliding Tackle',
               'min': 30,
               'max': 99,
               'default': 65,
               'step': None,
               'guide_title': '❓ How do I rate my Sliding Tackle?',
               'guide_md': 'Same logic as standing tackle, but specifically for slide challenges: '
                           'track attempted slide tackles vs. clean wins (ball won, no foul, you '
                           'recover quickly afterward).\n'
                           '\n'
                           '- **Frequently mistimed/fouls** → rate **30-50**\n'
                           '- **Sometimes clean, sometimes late** → rate **50-65**\n'
                           '- **Mostly clean and well-timed** → rate **65-80**\n'
                           '- **Consistently clean, good recovery afterward** → rate **80+**\n'
                           '\n'
                           'Note: many modern top defenders intentionally slide-tackle *less* than '
                           "older generations (higher foul/injury risk), so don't assume a low "
                           'attempt count means a low rating — judge purely on success rate when '
                           'you do commit.'},
              {'key': 'interceptions',
               'label': 'Interceptions',
               'min': 30,
               'max': 99,
               'default': 68,
               'step': None,
               'guide_title': '❓ How do I rate my Interceptions?',
               'guide_md': 'Track how often you read a pass and step in front of it *before* it '
                           'reaches its target, across a few games.\n'
                           '\n'
                           '- **Rarely anticipate passes** → rate **30-50**\n'
                           '- **Occasionally read the play, 1-2 real interceptions per game** → '
                           'rate **50-70**\n'
                           '- **Regularly reading passing lanes, 2-3+ per game** → rate **70-85**\n'
                           '- **Elite anticipation, routinely cuts out attacks before they '
                           'develop** → rate **85+**\n'
                           '\n'
                           'Professional defenders average roughly **1-3 interceptions per match** '
                           'as a baseline reference.\n'
                           '\n'
                           '[Defender metric '
                           'benchmarks](https://thepfsa.co.uk/10-essential-football-metrics-you-should-know/)'},
              {'key': 'physical',
               'label': 'Physical / Duel Strength',
               'min': 30,
               'max': 99,
               'default': 68,
               'step': None,
               'guide_title': '❓ How do I rate my Physicality?',
               'guide_md': 'This combines your strength (reuse your bench press result above) with '
                           'aggression/duel-winning — how you fare in physical, '
                           'shoulder-to-shoulder and aerial contests.\n'
                           '\n'
                           '- **Consistently loses physical duels/out-muscled** → rate **30-50**\n'
                           '- **Competitive but inconsistent in duels** → rate **50-70**\n'
                           '- **Wins most 50/50s and aerial duels** → rate **70-85**\n'
                           '- **Dominant physically, rarely beaten in a duel** → rate **85+**'},
              {'key': 'defensiveawareness',
               'label': 'Defensive Awareness',
               'min': 30,
               'max': 99,
               'default': 68,
               'step': None,
               'guide_title': '❓ How do I rate my Defensive Awareness?',
               'guide_md': 'This is about positioning and reading the game rather than any single '
                           'physical action — use this checklist from recent real games:\n'
                           '\n'
                           '- I rarely get caught out of position or beaten for pace on the last '
                           'line\n'
                           '- I recognize danger and adjust my position before the ball arrives, '
                           'not after\n'
                           '- I communicate and organize teammates around me\n'
                           "- I rarely commit to a challenge I don't need to make\n"
                           '- Coaches trust me in high-pressure defensive moments\n'
                           '\n'
                           '**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · **4-5 '
                           'true, consistently** → rate **70-90**'},
              {'key': 'headingaccuracy',
               'label': 'Heading Accuracy',
               'min': 30,
               'max': 99,
               'default': 65,
               'step': None,
               'guide_title': '❓ How do I rate my Heading Accuracy?',
               'guide_md': '**Objective anchor — aerial duel win rate.** Over a few games or '
                           'set-piece defending drills, track contested headers won vs. attempted '
                           '(both defending crosses and clearing set pieces).\n'
                           '\n'
                           '- **Under 40% win rate** → rate **30-50**\n'
                           '- **40-55% win rate** → rate **50-65**\n'
                           '- **55-70% win rate** → rate **65-80**\n'
                           '- **70%+ win rate (above pro top-flight average of ~66%)** → rate '
                           '**80+**\n'
                           '\n'
                           '[Aerial duel '
                           'benchmarks](https://www.athletepath.com/soccer-aerial-duel-calculator/)'},
              {'key': 'jumping',
               'label': 'Jumping',
               'min': 30,
               'max': 99,
               'default': 60,
               'step': None,
               'guide_title': '❓ How do I rate my Jumping?',
               'guide_md': '**Objective anchor — standing vertical jump.** Stand flat next to a '
                           'wall, mark your standing reach, jump straight up and mark your peak '
                           'reach. The difference is your vertical jump.\n'
                           '\n'
                           '- **Under 14 inches** → rate **30-50**\n'
                           '- **14-18 inches (average adult male range)** → rate **50-65**\n'
                           '- **18-24 inches (good athletic level)** → rate **65-80**\n'
                           '- **24+ inches (strong athletic level for a field-sport athlete)** → '
                           'rate **80+**\n'
                           '\n'
                           '[Vertical jump '
                           'norms](https://www.topendsports.com/testing/norms/vertical-jump.htm)'},
              {'key': 'composure',
               'label': 'Composure',
               'min': 30,
               'max': 99,
               'default': 65,
               'step': None,
               'guide_title': '❓ How do I rate my Composure?',
               'guide_md': 'For a defender, composure mostly shows up in how you handle pressure '
                           'near your own goal — use this checklist:\n'
                           '\n'
                           '- I can take a calm first touch under pressure in my own box\n'
                           "- I don't panic-clear the ball when I have time to play out\n"
                           "- A mistake doesn't rattle my next few defensive actions\n"
                           '- I stay calm and communicate even when the team is under sustained '
                           'pressure\n'
                           '- I make good decisions in the last few minutes of close games\n'
                           '\n'
                           '**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · **4-5 '
                           'true, consistently** → rate **70-90**'},
              {'key': 'passing',
               'label': 'Build-Up Passing',
               'min': 30,
               'max': 99,
               'default': 60,
               'step': None,
               'guide_title': '❓ How do I rate my Build-Up Passing?',
               'guide_md': 'Modern defenders are expected to play out from the back, not just '
                           'clear the ball. **Objective anchor — wall pass test:** 100 total '
                           'attempts (50 per foot) against a wall, count clean returns, same as a '
                           "midfielder's passing test.\n"
                           '\n'
                           '- **Under 50/100 clean** → rate **30-45**\n'
                           '- **50-70/100 clean** → rate **45-60**\n'
                           '- **70-85/100 clean** → rate **60-75**\n'
                           '- **85+/100 clean, comfortable playing out under pressure** → rate '
                           '**75+**\n'
                           '\n'
                           '[Wall pass '
                           'benchmarks](https://www.ritfitsports.com/blogs/article/how-to-improve-soccer-passing)'}]}
