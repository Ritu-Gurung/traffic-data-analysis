from graphics import*

print("Please enter the date in DD MM YYYY format!")

file1 = "traffic_data" + "15062024" + ".csv"
file2 = "traffic_data" + "16062024" + ".csv"
file3 = "traffic_data" + "21062024" + ".csv"

selected_dataset = " "

while True:  
    try:
        day = int(input("Enter date in the format DD: "))
        month = int(input("Enter month in the format MM: "))
        year = int(input("Enter year in the format YYYY: "))

        if not (1 <= day <= 31):
            print("Out of Range. Day must be in the range 1-31.")
            continue  

        if not (1 <= month <= 12):
            print("Out of Range. Month must be in the range 1-12.")
            continue  

        if not (2020 <= year <= 2024):
            print("Out of Range.Year must be in the range 2020-2024.")
            continue

        selected_date = f"{day:02d}{month:02d}{year}"
        selected_dataset = f"traffic_data{selected_date}.csv"


        #Initialize a 2D list to store vehicle data
        vehicle_data = []
        bicycles_per_hour ={}
        vehicles_per_hour_hanley = {}

        # Attempt to open the dataset
        try:
            with open(selected_dataset, "r") as file:
                content = file.readlines()

                #Initialize counters for required information
                total_vehicles = 0
                total_trucks = 0
                total_electric_vehicles = 0
                total_two_wheeled_vehicles = 0
                total_buses_north = 0
                total_straight_vehicles = 0
                total_over_speed_limit = 0
                total_vehicles_elm_junction = 0
                total_vehicles_hanley_junction = 0
                total_scooters = 0
                total_rainy_hours = 0

                #Process each line after the header
                for line in content[1:]:
                    columns = line.strip().split(",")

                    #Append each row of data to vehicle_data
                    vehicle_data.append(columns)

                    vehicle_type = columns[8].lower()

                    #Count total vehicles
                    total_vehicles +=1

                    #Count specific vehicle types
                    if vehicle_type == "truck":
                        total_trucks +=1

                    elif columns[9].strip() =="True":
                        total_electric_vehicles +=1

                    if vehicle_type in ["bicycle","scooter","motorcycle"]:
                        total_two_wheeled_vehicles +=1

                    if columns[0]=="Elm Avenue/Rabbit Road" and columns[4] == "N":
                        if vehicle_type == "buss":
                            total_buses_north +=1

                    if columns[3]==columns[4]:
                        total_straight_vehicles +=1

                    if columns[0] == "Elm Avenue/Rabbit Road":
                        total_vehicles_elm_junction +=1

                        if vehicle_type=="scooter":
                            total_scooters +=1

                    if total_vehicles_elm_junction >0:
                        percentage_scooters = round((total_scooters/total_vehicles_elm_junction)*100)
                    else:
                        percentage_scooters = 0
                        
                    if columns[0] == "Hanley Highway/Westway":
                        total_vehicles_hanley_junction +=1

                    rainy_condition = ["Light Rain", "Heavy Rain"]
                    weather_condition = columns[5].strip()
                    if weather_condition in rainy_condition:
                        total_rainy_hours +=1
                
                    #Count vehicles per hour for Hanley Highway/Westway
                    time_of_day = columns[2].strip()
                    hour = time_of_day.split(":")[0]
                    if hour not in vehicles_per_hour_hanley:
                        vehicles_per_hour_hanley[hour] =0
                    vehicles_per_hour_hanley[hour] +=1

                    vehicle_speed = float(columns[7])
                    speed_limit =  float(columns[6])

                    if vehicle_speed > speed_limit:
                        total_over_speed_limit +=1
                    
                    #Determine peak hour on Hanley Highway/Westway
                    peak_hour_count = 0
                    peak_hours = []

                    for hour,count in vehicles_per_hour_hanley.items():
                        if count > peak_hour_count:
                            peak_hour_count = count
                            peak_hours = [hour]
                        elif count == peak_hour_count:
                            peak_hours.append(hour)

                    #print peak hour(s)
                    if peak_hour_count >0:
                        for hour in peak_hours:
                            next_hour = f"{(int(hour) +1)%24:02}"

                    if total_vehicles >0:
                        percentage_trucks = round((total_trucks/total_vehicles)*100)
                    else:
                        percentage_trucks = 0

                    if vehicle_type == "bicycle":
                        time_of_day  = columns[2].strip()
                        hour = time_of_day.split(":")[0]
                        if hour not in bicycles_per_hour:
                            bicycles_per_hour[hour] = 0
                        bicycles_per_hour[hour] +=1
                

                total_bicycles = sum(bicycles_per_hour.values())
                total_hours = len(bicycles_per_hour)

                if total_hours >0:
                    average_bicycles_per_hour = round(total_bicycles/total_hours)
                else:
                    average_bicycles_per_hour = 0

                with open("results.txt", "a") as results_file:

                    output_lines = [ 
                        f"Data file selected is {selected_dataset}:",
                        f"The total number of vehicles recorded for this date is {total_vehicles}.",
                        f"The total number of trucks recorded for this date is {total_trucks}.",
                        f"The total number of electric vehicles for this date is {total_electric_vehicles}.",
                        f"The total number of two wheeled vehicles for this date is {total_two_wheeled_vehicles}.",
                        f"The total number of buses leaving Elm Avenue/Rabbit Road junction heading north is {total_buses_north}.",
                        f"The total number of vehicles passing through both junctions without turning left or right is {total_straight_vehicles}.",
                        f"The percentage of total vehicles recorded that are trucks is {percentage_trucks}%.",
                        f"The average number of bicycles per hour is {average_bicycles_per_hour}.",
                        f"The total number of vehicles recorded as over the speed is {total_over_speed_limit}.",
                        f"The total number of vehicles passing through ELm Avenue/Rabbit Road junction is {total_vehicles_elm_junction}.",
                        f"The total number of vehicles passing through ELm Avenue/Rabbit Road junction is {total_vehicles_hanley_junction}.",
                        f"The percentage of scooters passing through Elm Avenue/Rabbit Road is {percentage_scooters}%.",
                        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {peak_hour_count}.",
                        f"The most vehicles through Hanley Highway/Westway were recorded between {hour}:00 and {next_hour}:00.",
                        f"The number of hours of rain for this date is {total_rainy_hours}."]

                    for line in output_lines:
                        print(line)
                        results_file.write(line + "\n")
                    results_file.write(" *********************************** \n")


                    run_again = input("Do you want to load a new dataset? (y/n): ").strip().lower()
                    if run_again != "y":
                        break

        except FileNotFoundError:
            print(f"The dataset {selected_dataset} does not exist. Please try again!")
        continue

    except ValueError:
        print("Integer Required!")

def draw_histogram():
                    hourly_data = {}
                    selected_dataset = f"traffic_data{selected_date}.csv"  

                    try:
                        with open(selected_dataset, "r") as file:
                            content = file.readlines()[1:] 
                            # Process each row in the provided data
                            for row in content:
                                columns = row.strip().split(",")  
                                time_of_day = columns[2]  
                                junction = columns[0]  

                                hour = time_of_day.split(":")[0]  
                                key = (junction, hour)  

                                # Increment the count for the specific junction and hour
                                if key not in hourly_data:
                                    hourly_data[key] = 0
                                hourly_data[key] += 1

                    except FileNotFoundError:
                        print(f"The dataset {selected_dataset} does not exist.")
                        return

                    # get unique junctions and hours
                    junctions = list({key[0] for key in hourly_data.keys()})
                    if len(junctions) < 2:
                        print("Not enough junctions for the plot.")
                        return

                    # Sort data by hours for each junction
                    hours = [f"{hour:02}" for hour in range(24)]
                    junction1, junction2 = junctions[:2]
                    junction1_data = [hourly_data.get((junction1, hour), 0) for hour in hours]
                    junction2_data = [hourly_data.get((junction2, hour), 0) for hour in hours]

                    win = GraphWin("Histogram of Vehicle Frequency per Hour", 1000, 600)
                    win.setBackground("white")

                    title = Text(Point(500, 30), f"Histogram of Vehicle Frequency per Hour on {selected_date}")
                    title.setSize(16)
                    title.setStyle("bold")
                    title.draw(win)

                    # Draw axes
                    x_axis = Line(Point(80, 550), Point(920, 550))
                    y_axis = Line(Point(80, 550), Point(80, 50))
                    x_axis.draw(win)
                    y_axis.draw(win)

                    # X-axis labels (hours)
                    for i, hour in enumerate(hours):
                        x_label = Text(Point(110 + i * 35, 570), hour)
                        x_label.setSize(8)
                        x_label.draw(win)

                    # Y-axis gridlines and labels
                    max_frequency = max(junction1_data + junction2_data)
                    scale_factor = 400 / max_frequency if max_frequency > 0 else 1

                    for i in range(0, max_frequency + 1, max(1, max_frequency // 10)):
                        y = 550 - i * scale_factor
                        y_label = Text(Point(50, y), str(i))
                        y_label.setSize(8)
                        y_label.draw(win)
                        gridline = Line(Point(80, y), Point(920, y))
                        gridline.setFill("lightgray")
                        gridline.draw(win)

                    # Draw bars
                    bar_width = 12
                    for i, hour in enumerate(hours):
                        # Junction 1 bar
                        j1_height = junction1_data[i] * scale_factor
                        j1_bar = Rectangle(Point(110 + i * 35 - bar_width, 550), Point(110 + i * 35, 550 - j1_height))
                        j1_bar.setFill("limegreen")
                        j1_bar.draw(win)

                        if j1_height > 0:
                            j1_label = Text(Point(110 + i * 35 - bar_width / 2, 550 - j1_height - 10), str(junction1_data[i]))
                            j1_label.setSize(8)
                            j1_label.draw(win)

                        # Junction 2 bar
                        j2_height = junction2_data[i] * scale_factor
                        j2_bar = Rectangle(Point(110 + i * 35, 550), Point(110 + i * 35 + bar_width, 550 - j2_height))
                        j2_bar.setFill("purple")
                        j2_bar.draw(win)

                        if j2_height > 0:
                            j2_label = Text(Point(110 + i * 35 + bar_width / 2, 550 - j2_height - 10), str(junction2_data[i]))
                            j2_label.setSize(8)
                            j2_label.draw(win)

                    legend_start_y = 100
                    legend1_box = Rectangle(Point(830, legend_start_y), Point(850, legend_start_y + 15))
                    legend1_box.setFill("limegreen")
                    legend1_box.draw(win)
                    legend1_text = Text(Point(920, legend_start_y + 7.5), junction1)
                    legend1_text.setSize(10)
                    legend1_text.draw(win)

                    legend2_box = Rectangle(Point(830, legend_start_y + 25), Point(850, legend_start_y + 40))
                    legend2_box.setFill("purple")
                    legend2_box.draw(win)
                    legend2_text = Text(Point(920, legend_start_y + 32.5), junction2)
                    legend2_text.setSize(10)
                    legend2_text.draw(win)

                    win.getMouse()
                    win.close()

draw_histogram()



        








    
