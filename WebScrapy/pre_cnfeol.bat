ECHO OFF

set /a date=%date:~0,4%%date:~5,2%%date:~8,2%-1
echo %date%

SET TodayYear=%date:~0,4%
SET TodayMonthP0=%date:~4,2%
SET TodayDayP0=%date:~6,2%

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
echo %s_today%
REM python test3.py %s_today%
python scrp_cnfeol.py %TodayYear%%TodayMonthP0%%TodayDayP0%

PAUSE