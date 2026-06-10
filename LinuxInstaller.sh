#!/bin/bash
pyinstaller SeedNexusData.spec --distpath executable --workpath temp_seed_build
pyinstaller NexusHotel.spec --distpath executable --workpath temp_build
rm -rf temp_seed_build
rm -rf temp_build
echo "Builds complete."
