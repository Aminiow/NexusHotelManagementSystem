@echo off
pyinstaller SeedNexusData.spec --distpath executable --workpath temp_seed_build
pyinstaller NexusHotel.spec --distpath executable --workpath temp_build
rmdir /s /q temp_seed_build
rmdir /s /q temp_build
echo Builds complete.
pause
