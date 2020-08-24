ECHO OFF

SET TodayYear=%date:~0,4%
SET TodayMonthP0=%date:~5,2%
SET TodayDayP0=%date:~8,2%

IF %TodayMonthP0:~0,1% == 0 (
	SET /A TodayMonth=%TodayMonthP0:~1,1%+0
) ELSE (
	SET /A TodayMonth=TodayMonthP0+0
)

IF %TodayMonthP0:~0,1% == 0 (
	SET /A TodayDay=%TodayDayP0:~1,1%+0
) ELSE (
	SET /A TodayDay=TodayDayP0+0
)

set s_today=%TodayYear%%TodayMonthP0%%TodayDayP0%
REM python stock_run.py %s_today%
python stock_run.zip %TodayYear%%TodayMonthP0%%TodayDayP0%

PAUSE



