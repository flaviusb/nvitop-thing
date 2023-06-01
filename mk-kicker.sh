#!/bin/bash

kicker="kick.sh"
base="~/nvitop-thing/"
venv="foo"
log="/var/log/gpuusage/gpu-usage.log"

usage() { cat <<HELP
mk-kicker.sh: Generates a shell script that, when run, runs the logger if it is not already running.
Options:
  --help    Shows this text
  --kicker  Filename for the generated script
  --base    PATH to the directory the logger is in
  --venv    The name of the venv or virtualenv
  --log     Full PATH to the log location

Any argument not given will use a default value.

HELP
exit 0;
}

while [[ $# > 0 ]]; do
    if [ $# = 1 ]; then
      opt="$1"
      case "${opt}" in
        -h)
          usage
          ;;
        --help)
          usage
          ;;
        *)
          echo "I don't understand: $opt by itself"
          exit 1
          ;;
      esac
    fi
    opt="$1"
    value="$2"
    case "${opt}" in
      --kicker)
        kicker="$value"
        shift
        shift
        ;;
      --base)
        base="$value"
        shift
        shift
        ;;
      --venv)
        venv="$value"
        shift
        shift
        ;;
      --log)
        log="$value"
        shift
        shift
        ;;
      *)
        echo "I don't understand: $opt"
        exit 1
        ;;
    esac
done

cat > "$kicker" <<blerg
#!/bin/bash

running() {
  ps -C python3 -o args= | grep --quiet "logging-script-thing.py"
}
if running
then
  echo Already running
else
  alias python3=python3.9
  alias pip3=pip3.9
  cd "$base"
  . "$venv/bin/activate"
  python3 logging-script-thing.py "$log"
fi

blerg

chmod u+x "$kicker"

