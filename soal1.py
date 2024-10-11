import re
from datetime import datetime
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter

def parse_file(filename):
    timestamps = []
    speeds = []
    current_timestamp = None

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("Timestamp:"):
                current_timestamp = datetime.strptime(line.split(": ")[1].strip(), "%Y-%m-%d %H:%M:%S")
            elif "sender" in line:
                speed_match = re.search(r"(\d+\.?\d*)\s+([KMG])bits/sec", line)
                if speed_match:
                    speed = float(speed_match.group(1))
                    unit = speed_match.group(2)
                    if unit == 'K':
                        speed *= 1e-3
                    elif unit == 'G':
                        speed *= 1e3
                    timestamps.append(current_timestamp)
                    speeds.append(speed)

    return timestamps, speeds

def create_chart(timestamps, speeds):
    source = ColumnDataSource(data=dict(
        timestamp=timestamps,
        speed=speeds,
        formatted_timestamp=[ts.strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps]
    ))

    p = figure(title="Testing Jaringan", x_axis_label='Timestamp', y_axis_label='Speed (Mbits/sec)',
               x_axis_type='datetime', width=1200, height=600)

    p.line('timestamp', 'speed', line_width=2, color='navy', alpha=0.8, source=source)
    p.scatter(x='timestamp', y='speed', size=8, color='navy', alpha=0.5, source=source)

    hover = HoverTool(tooltips=[
        ("Timestamp", "@formatted_timestamp"),
        ("Speed", "@speed{0.00} Mbits/sec")
    ])
    p.add_tools(hover)

   
    p.xaxis.formatter = DatetimeTickFormatter(
        seconds="%Y-%m-%d %H:%M:%S",
        minutes="%Y-%m-%d %H:%M:%S",
        hours="%Y-%m-%d %H:%M:%S",
        days="%Y-%m-%d %H:%M:%S",
        months="%Y-%m-%d %H:%M:%S",
        years="%Y-%m-%d %H:%M:%S"
    )

   
    p.xaxis.major_label_orientation = 0.7

    return p

def main():
    filename = "soal_chart_bokeh.txt"
    timestamps, speeds = parse_file(filename)
    
    chart = create_chart(timestamps, speeds)
    
    output_file("soal1.html")
    show(chart)

if __name__ == "__main__":
    main()