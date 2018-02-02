//Automatically Added
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

// Things I added
using WMPLib;
using AxWMPLib;

namespace GUI_Csharp2
{
    public partial class GUI_Csharp : Form
    {
        List<string> videoNames = new List<string>(); // List of videos
        List<string> graphNames = new List<string>(); // List of graphs

        public GUI_Csharp()
        {
            InitializeComponent();
        }

        //Load button
        private void loadToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Loading Videos
            toolStripStatusLabel1.Text = "Loading Videos";

            //Clearing the list and filling it with blanks
            videoNames.Clear();
            for (int i = 0; i < 4; i++)
            {
                videoNames.Add("");
            }

            //Select Settings
            openFileDialog1.Multiselect = true;

            //Instructions
            MessageBox.Show("Please select the videos in order, to select the videos hold ctrl and click");

            //Opening and running dialog
            DialogResult dr = openFileDialog1.ShowDialog();
            if (dr == System.Windows.Forms.DialogResult.OK)
            {
                foreach (String file in openFileDialog1.FileNames)
                {
                    //Get each file name and add it to the videoNames list
                    int j=0;
                    string name = file;
                    videoNames[j] = name;
                    j++;

                }
            }

            //Loading graphs
            toolStripStatusLabel1.Text = "Loading Graphs";

            //Clearing the list and filling with blanks
            graphNames.Clear();
            for(int i =0; i<3; i++)
            {
                graphNames.Add("");
            }

            //Select settings
            openFileDialog1.Multiselect = true;

            //Instructions
            MessageBox.Show("Please select the graphs in order, to select the videos hold ctrl and click");

            //Opening and Running the Dialog
            DialogResult dr2 = openFileDialog1.ShowDialog();
            if (dr2 == System.Windows.Forms.DialogResult.OK)
            {
                foreach (String file in openFileDialog1.FileNames)
                {
                    //Getting the files and adding to the graphNames list
                    int k=0;
                    string name = file;
                    graphNames[k] = name;
                    k++;

                }
            }

            //Setting the graph boxes to show the graphs
            pictureBox1.ImageLocation = graphNames[0];
            pictureBox2.ImageLocation = graphNames[1];
            pictureBox3.ImageLocation = graphNames[2];

        }

        //Calibration button
        private void calibrateToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Calibrate";
            System.Diagnostics.Process.Start("CMD.exe");
        }

        //Record Video Button
        private void rToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Recording";
            System.Diagnostics.Process.Start("CMD.exe");
        }

        //Analyse Buttonn
        private void analyseToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Begin Analyse
            toolStripStatusLabel1.Text = "Analysing";

            //Opening up a CMD
            System.Diagnostics.Process process = new System.Diagnostics.Process();
            System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();

            //Hides the CMD
            startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;

            //Assigning the properties
            startInfo.FileName = "CMD.exe";

            //Sets the text into the CMD, '/C' intialisees the command and then closes the CMD
            startInfo.Arguments = "/C C:\\Python27\\pythonw.exe C:\\Users\\Chun_\\EDP\\gait-lab\\detection\\detect.py";
            process.StartInfo = startInfo;
            process.Start();
        }

        //Play button
        private void Play_button_Click(object sender, EventArgs e)
        {
            videoDisplay.Ctlcontrols.play();
        }

        //Pause Button
        private void pause_button_Click(object sender, EventArgs e)
        {
            videoDisplay.Ctlcontrols.pause();
        }

        //Back Step button
        private void prev_button_Click(object sender, EventArgs e)
        {
            //Contorl casting
            IWMPControls2 Ctlcontrols2 = (IWMPControls2)videoDisplay.Ctlcontrols;
            Ctlcontrols2.step(-1);
        }

        //Forward frame button
        private void next_button_Click(object sender, EventArgs e)
        {
            //Control casting
            IWMPControls2 Ctlcontrols2 = (IWMPControls2)videoDisplay.Ctlcontrols;
            Ctlcontrols2.step(1);
        }

        //Change to Video 1
        private void videoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[0];
            videoLabel.Text = "Video 1";
        }

        //Change to Video 2
        private void video2ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[1];
            videoLabel.Text = "Video 2";
        }

        //Change to Video 3
        private void video3ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[2];
            videoLabel.Text = "Video 3";
        }

        //Change to Video 4
        private void video4ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[3];
            videoLabel.Text = "Video 4";
        }

        //Help functions
        private void loadToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This will allow you to laod a previous session.");
        }

        private void calibrateToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This will calibrate the cameras in pairs, you will need to do each pair individually.");
        }

        private void recordToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This will begin the video recording.");
        }

        private void analyseToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This will begin the analysis of the footage and will automatically make graphs.");
        }

        private void videosToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("You can choose which video to show on in the player.");
        }

        private void increaseAccuracyToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Marker detection during analysis will be more accurate, however the analysis will be slower.");
        }

        private void playToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Will play the video.");
        }

        private void pauseToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Will pause the video.");
        }

        private void toolStripMenuItem2_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Will go back one second in the video.");
        }

        private void toolStripMenuItem3_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Will go forward by one frame.");
        }

        private void trunkSwayToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Trunk Sway is the movement of the hips as you walk.");
        }

        private void kneeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("The figures shown here are the angles of the respective knee.");
        }

        private void printToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("This will print the selected graph.");
        }

    }
}
