//Automatically Added
using System;
using System.Collections.Generic;
using System.Windows.Forms;

// Things I added
using WMPLib;
using System.Drawing.Printing;

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
            //counters
            int g = 0;
            int v = 0;
            //Loading Videos
            toolStripStatusLabel1.Text = "Loading Videos";

            videoNames.Clear();
            if(videoNames.Count == 0)
            {
                Intialise(videoNames, 4);
            }
            Fill(videoNames);

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
                    string name = file;
                    videoNames[v] = name;
                    v++;
                }
            }

            //Loading graphs
            toolStripStatusLabel1.Text = "Loading Graphs";

            graphNames.Clear();
            if(graphNames.Count == 0)
            {
                Intialise(graphNames, 2);
            }
            Fill(graphNames);

            //Clearing the list and filling with blanks
            graphNames.Clear();
            for(int i =0; i<2; i++)
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
                    string name = file;
                    graphNames[g] = name;
                    g++;
                }
            }

            //Setting the graph boxes to show the graphs
            pictureBox1.ImageLocation = graphNames[0];
            pictureBox2.ImageLocation = graphNames[1];

            toolStripStatusLabel1.Text = "";

        }

        //Calibration button
        private void calibrateToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Calibrate";
            System.Diagnostics.Process.Start("CMD.exe");

            //Opening up a CMD
            System.Diagnostics.Process process = new System.Diagnostics.Process();
            System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();

            //Hides the CMD
            //startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;

            //Assigning the properties
            startInfo.FileName = "CMD.exe";

            //Sets the text into the CMD, '/C' intialisees the command and then closes the CMD
            startInfo.Arguments = "/K C:\\Gait-Lab\\resources\\cameracal\\x64\\Release\\cameracal.exe";
            process.StartInfo = startInfo;
            process.Start();

            toolStripStatusLabel1.Text = "Calibration Finished";
        }

        //Record Video Button
        private void rToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Recording";
            System.Diagnostics.Process.Start("CMD.exe");

            toolStripStatusLabel1.Text = "";
        }

        //Analyse Buttonn
        private void analyseToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Begin Analyse
            toolStripStatusLabel1.Text = "Analysing";

            //Marker Detection
            //Opening up a CMD
            System.Diagnostics.Process process = new System.Diagnostics.Process();
            System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();

            //Hides the CMD
            //startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;

            //Assigning the properties
            startInfo.FileName = "CMD.exe";

            //Sets the text into the CMD, '/C' intialisees the command and then closes the CMD
            //This is for the python, call python then the call the module then the directory of the video
            startInfo.Arguments = "/C C:\\Python27\\pythonw.exe C:\\Users\\Chun_\\EDP\\gait-lab\\detection\\modular_detect.py --video C:\\Users\\Chun_\\EDP\\gait-lab\\gui\\GUI_Csharp2\\testSession1\\Video5.mp4";
            process.StartInfo = startInfo;
            process.Start();

            //Joint angle calculation
            //Opening up a CMD
            System.Diagnostics.Process joints = new System.Diagnostics.Process();
            System.Diagnostics.ProcessStartInfo cal = new System.Diagnostics.ProcessStartInfo();

            //Assigning the properties
            cal.FileName = "CMD.exe";

            cal.Arguments = "/C C:\\Gait-Lab\\resources\\3d_pos\\x64\\Release\\3d_pos.exe";
            joints.StartInfo = cal;
            joints.Start();

            toolStripStatusLabel1.Text = "Finished Analysis";
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
            MessageBox.Show("This will calibrate the cameras.");
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

        private void printMenu_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Printing";

            PrintDialog printDialog1 = new PrintDialog();
            printDialog1.ShowDialog();

            PrintDocument printDoc = new PrintDocument();
        }
    }
}
