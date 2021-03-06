import time
import os
import datetime as dt

import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from PIL import Image

import data_handler as dh

st.set_page_config(page_title="RetroPark - CIED EE/CpE Senior Design Team 5",
                   page_icon="./Front End Display/RetroPark_Logo_mini.jpg",
                   menu_items={'Get Help': None, 'Report a bug': None, 'About': None})
# Update frequency in seconds
update_freq = 30

# Team Image
logo = Image.open("./Front End Display/RetroPark_Logo.png")

st.image(logo, caption="Spring 2020/Fall 2021 EE/CpE Senior Design Team 5")
# st.header("EE-CPE 2021 Design Team 5")

# Create Demo Data Display
st.subheader("Ximenes Parking Lot - Small Scale Demo")

# Place data in a container
data_container = st.empty()

while True:
    with data_container.container():
        latest_update_time = dt.datetime.now()
        next_update_time = latest_update_time + dt.timedelta(0, 30)
        latest_update_time = latest_update_time.strftime("%H:%M:%S")
        next_update_time = next_update_time.strftime("%H:%M:%S")

        with st.spinner("Grabbing Occupancy Data..."):
            total_spots, vacant_spots, occupied_spots, occupancy_percent, timestamp, current_filepath = dh.import_occupancy_data(
                './Front End Display/remote_db/')
        st.success("Occupancy Data Up to Date as of {}, Last Checked at {}, Checking again at {}".format(timestamp,
                                                                                                         latest_update_time,
                                                                                                         next_update_time))
        dcol1, dcol2, dcol3, dcol4 = st.columns(4)
        # Update this in real time
        dcol1.metric(label="Current Occupancy %", value="{:.2f}%".format(occupancy_percent), delta_color="inverse")
        dcol2.metric(label="Vacant Spots", value="{}/{}".format(vacant_spots, total_spots), delta_color="inverse")
        dcol3.metric(label="Occupied Spots", value="{}/{}".format(occupied_spots, total_spots), delta_color="inverse")

        # Spacers
        dcol3.markdown("")

        # Load lot diagram
        lot_diag = Image.open('./Front End Display/.current_diag.jpg')
        st.image(lot_diag, caption="Current Spot Occupancy as of {}.".format(timestamp))

        # Create Expanders
        st.subheader("Explore More of Our Project")
        # map_display = st.expander(label="Show Map")
        current_data = st.expander(label="Raw Data")
        about_per = st.expander(label="About Neural Net Personas")
        about_rt = st.expander(label="About RetroPark")
        about_us = st.expander(label="About Team 5")
        diagnostic = st.expander(label="Neural Net Statistics")
        schematics = st.expander(label="Functional Block and Software Diagram")
        acknowledge = st.expander(label="Acknowledgements")

        # Populate each expander with data
        with about_rt:
            st.header("What is RetroPark?")
            st.markdown(
                "RetroPark is the colloquial name given to The University of Texas at San Antonio's EE/CpE 2021 Senior Design Team 5. We consist of Patrick Cavanagh, Gisselle Contreras-Velarde, and Will Sanchez. The goal of our project is to create the Parking Occupancy Monitor, or POM. This device tracks the live occupancy of individual parking spots and sends it to a cloud based server to then display it to you here!")
            st.header("What is the POM?")
            st.markdown(
                "The Parking Occupancy Monitor (POM) is a device that will track live parking occupancy to a high degree in flat parking lots using a series of Tensorflow Convolutional Neural Networks. Current occupancy solutions either rely on controlled entrances and exits or sensors placed in each individual spot. The Parking Occupancy Monitor tracks a given set of parking spots optically using an Infrared Camera and Infrared Flash. To enable a high degree of accuracy at all times of the day, each spot can be fitted with a retro-reflective target to help determine spot occupancy.")
        with about_us:
            st.header("We are RetroPark")
            col1, col2, col3 = st.columns(3)
            patrick = Image.open("./Front End Display/patrick.png")
            gisselle = Image.open("./Front End Display/gisselle.png")
            will = Image.open("./Front End Display/will.png")

            col1.image(patrick, caption="Patrick Cavanagh - CpE")
            col1.subheader("Lead Designer")
            col1.markdown(
                "The Parking Occupancy Monitor is the brainchild of Patrick. As Lead Designer, Patrick was responsible for conceptualizing the POM and leading the team through the design and implementation of the neural network as well as the software required to calibrate the parking lot data, isolate individual parking spots into individual images which is then passed to the neural network for abstract individual spot detection. Additionally, Patrick was responsible for the central server that receives occupancy data from POMs and displays it live to a webpage.")
            col1.markdown("[LinkedIn](https://www.linkedin.com/in/patrickc-pc/)")

            col2.image(gisselle, caption="Gisselle Contreras-Velarde - EE")
            col2.subheader("Project Admin")
            col2.markdown(
                "Gisselle ensured timelines were being followed by updating a list of upcoming tasks and updating teammates. She also administered communications with the needed parties such as makerspace and parking services. Gisselle finalized the creation of the project's enclosure by taking the measurements of outlets and following up on the status of it with the makerspace.")
            col2.markdown("[LinkedIn](https://www.linkedin.com/in/gisselle-contreras-62aa90193/)")

            col3.image(will, caption="Will Sanchez - CpE")
            col3.subheader("Project Technician")
            col3.markdown(
                "Will acted as the project technician by helping complete needed tasks such as working on correspondence for weekly assignments, purchasing all need hardware for the design, and design and fabrication of various assemblies such as retroreflective targets for trial runs of software.")
            col3.markdown("[LinkedIn](https://www.linkedin.com/in/will-sanchez-758066b/)")
        with about_per:
            st.header("Neural Net Personas")
            st.subheader("Whats a persona?")
            st.markdown(
                "When the Parking Occupancy Monitor takes a photo to collect occupancy data, the photo is first split up into its individual parking spots and then processed depending on which persona is going to evaluate it. Each of the following personas is in reality a separately trained convolutional neural network; that is each persona does the same job but in a slightly different way.")
            col1, col2, col3 = st.columns(3)
            tom = Image.open("./Front End Display/tom.jpg")
            jerry = Image.open("./Front End Display/jerry.jpg")
            tweety = Image.open("./Front End Display/tweety.png")

            col1.image(tom, width=177)
            col1.markdown("*Tom - Grayscale Image Detection*")
            col1.markdown(
                "Tom is the first neural network that was created, but that does not make him the simplest. He is fed the least processed images, essentially seeing what the human eye sees, but due to this Tom needs to do a lot more work to determine spot vacancy.")

            col2.image(jerry, width=200)
            col2.markdown("*Jerry - Canny Edge Detection*")
            col2.markdown(
                "Jerry thinks a bit harder than Tom, but deep down hes not nearly as complex. Jerry first processes the input image with a Canny Edge Detection algorithm, this means that Jerry essentially just sees the edges of objects and uses that to determine if the spot is vacant.")

            col3.image(tweety, width=153)
            col3.markdown("*Tweety - Sobel X/Y Edge Detection*")
            col3.markdown(
                "Tweety is a bit of a wildcard; while he also performs an edge detection algorithm on the image before evaluating it, he instead uses a Sobel X/Y edge detection. To a human, the resulting image tends to look like jumbled garbage, but somewhere deep in the mind of Tweety he is able to take that garbage and tell you if there is a car present.")
        with current_data:
            st.dataframe(pd.read_csv(current_filepath))
            st.markdown("Shown above is the raw data that is received from the POM, each spotID has data regarding its status. Explanations of each column is listed below. ")
            st.markdown("**spotID:** Assigned unique ID per spot")
            st.markdown("**Judgement:** Whether or not the spot is occupied (occ) or not occupied (nocc)")
            st.markdown("**Confidence:** Average confidence in the answer from the Quorum")
            st.markdown("**Tug:** Result of the tug algorithm that chose the resulting Judgement, Negative is occ/Positive is nocc. The Magnitude represents a form of confidence.")
            st.markdown("**dtime:** How long it took for the POM to calculate the occupancy status")
            st.markdown("**tom_conf:** Tom's specific confidence in the given answer")
            st.markdown("**jerry_conf:** Jerry's specific confidence in the given answer")
            st.markdown("**tweety_conf:** Tweety's specific confidence in the given answer")

        with diagnostic:
            dcol1, dcol2 = st.columns(2)

            dcol1.metric(label="Training Accuracy", value="98.1%", delta="-0.1%")
            dcol2.metric(label="Validation Accuracy", value="96.2%", delta="0.2%")

            dcol1.metric(label="Training Loss", value="0.21%", delta="1.3%", delta_color="inverse")
            dcol2.metric(label="Validation Loss", value="0.14%", delta="-0.8%", delta_color="inverse")
        with schematics:
            functional = Image.open("./Front End Display/functional.png")
            software = Image.open("./Front End Display/software.png")
            server_software = Image.open("./Front End Display/serversoftware.png")
            st.image(functional, caption="Functional Block Diagram")
            st.image(software, caption="Software Block Diagram")
            st.image(server_software, caption="Server Software Block Diagram")
        with acknowledge:
            st.header("Special Thanks to the Following")
            st.write("Professor Patrick Benavidez")
            st.write("Chad Webster")
            st.write("Alberto Samaniego")
            st.write("David Kuenstler")
            st.write("Rachael Printz")
            st.write("UTSA College of Engineering and Integrated Design")
            st.write("Department of Electrical and Computer Engineering")

        delta_update = 0
        # Place data in a container
        update_container = dcol4.empty()
        while delta_update < update_freq:
            with update_container.container():
                st.markdown("T- Next Update")
                st.markdown("{} seconds".format(update_freq - delta_update))
                st.progress(delta_update / update_freq)
                time.sleep(1)
                delta_update += 1
                update_container.empty()
    data_container.empty()
