import os
import argparse
import rospy
import rosbag

def main():
    parser = argparse.ArgumentParser(description="Extract radar data from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_file", help="Output .txt file.")
    parser.add_argument("radar_topic", help="Radar topic.")

    args = parser.parse_args()

    print("Extract radar data from %s on topic %s into %s" % (args.bag_file,args.radar_topic, args.output_file))

    bag = rosbag.Bag(args.bag_file, "r")
    with open(args.output_file, 'w') as f:
        for topic, msg, t in bag.read_messages(topics=[args.radar_topic]):
            # Access frame_id from the message header
            frame_id = msg.header.frame_id
            # Write frame_id, x, y, z to the output file
            f.write("%s,%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n" % (
                    frame_id, msg.radar_frame_idx, msg.point_id, msg.x, msg.y, msg.z, msg.range,
                    msg.velocity, msg.doppler_bin, msg.bearing, msg.intensity,
                    msg.intensity_snr_noise, msg.noise, msg.time_human))

    print("Wrote radar data to %s" % args.output_file)

if __name__ == "__main__":
    main()

