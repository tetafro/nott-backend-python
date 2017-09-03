#!/bin/bash
#
# Make archive with the app ready for uploading to server
#

# Show progress bar
function show_progress {
    end=$1
    msg=$2
    # Spaces to hide previous message
    spaces='                        '
    for i in `seq 1 4 $end`; do
        echo -n █
    done
    if [ $end -lt 100 ]; then
        for i in `seq $(($end+1)) 4 100`; do
            echo -n ░
        done
        echo -n -e " $end% ($msg)$spaces\r"
    else
        echo -e " $end% ($msg)$spaces"
    fi
}

# Start timer
time_start=$((`date +%s`*1000+`date +%-N`/1000000))

if [ ! -d ./project ]; then
    echo 'Project not found!'
    exit
fi

install_dir=./install
django_settings=$install_dir/nott/core/settings.py
pass_ini=./pass.ini

show_progress 0 'Cleaning previous runs'
rm -rf $install_dir

show_progress 8 'Building javascript app'
docker-compose \
    -f docker-compose-dev.yml \
    run \
    --rm \
    frontend \
    webpack \
    1> /dev/null

show_progress 44 'Copying project'
mkdir -p $install_dir
cp -R ./project $install_dir/nott

show_progress 72 'Removing python cache'
find $install_dir \
    -name '__pycache__' \
    -type d \
    -exec rm -rf {} \; 2>/dev/null

show_progress 76 'Removing javascript sources'
for name in $(ls $install_dir/nott/public/js/); do
    if [ $name != "app.min.js" ]; then
        rm -rf $name
    fi
done

show_progress 80 'Setting passwords from file'
# Parse passwords file
function get_ini {
    str=$(grep -o '^'$1':.*$' $pass_ini)
    str=${str#*:}
    printf -v str "%q" $str
    echo $str
}
django_csrf=$(get_ini django_csrf)
db_user=$(get_ini db_user)
db_pass=$(get_ini db_pass)

# Put parsed values to project files
# Django CSRF key
sed -i 's/^SECRET_KEY = '\''.*'\''/SECRET_KEY = '\'$django_csrf\''/' $django_settings
# DB username
sed -i 's/^        '\''USER'\'': '\''.*'\'',/        '\''USER'\'': '\'$db_user\'',/' $django_settings
# DB password
sed -i 's/^        '\''PASSWORD'\'': '\''.*'\'',/        '\''PASSWORD'\'': '\'$db_pass\'',/' $django_settings

show_progress 84 'Compressing'
tar -zcf $install_dir/nott.tar.gz -C $install_dir nott

show_progress 96 'Cleaning'
rm -rf $install_dir/nott

show_progress 100 'Complete'

# Calculate time
time_end=$((`date +%s`*1000+`date +%-N`/1000000))
time_progress_ms=$(($time_end - $time_start))  # miliseconds
time_progress=$(echo "scale=3; $time_progress_ms/1000" | bc | sed 's/^\./0./')  # seconds

echo "Time in progress: $time_progress sec"
