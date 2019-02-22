ls json/*.json | while read name; do
  content="$(/home/redhog/.local/bin/jsonedit --scalar '$.results[0].body.export_view.value' < $name)"
  id="$(/home/redhog/.local/bin/jsonedit --scalar --first '$.results[0].id' < $name)"
  title="$(/home/redhog/.local/bin/jsonedit --scalar --first '$.results[0].title' < $name | sed -e "s+/+-+g")"
  echo "$content" > "txt/$title.txt"
  echo "$id" > "ids/$title.id"
done
