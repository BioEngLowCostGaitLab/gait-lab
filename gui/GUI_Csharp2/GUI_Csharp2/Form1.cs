using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

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

        private void loadToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Loading Videos
            toolStripStatusLabel1.Text = "Loading Videos";
            videoNames.Clear();
            openFileDialog1.Multiselect = true;

            MessageBox.Show("Please select the videos in order, to select the videos hold ctrl and click");
            DialogResult dr = openFileDialog1.ShowDialog();
            if (dr == System.Windows.Forms.DialogResult.OK)
            {
                foreach (String file in openFileDialog1.FileNames)
                {
                    string name = file;
                    videoNames.Add(name);

                }
            }
            //Loading graphs
            toolStripStatusLabel1.Text = "Loading Graphs";
            graphNames.Clear();
            openFileDialog1.Multiselect = true;

            MessageBox.Show("Please select the graphs in order, to select the videos hold ctrl and click");
            DialogResult dr2 = openFileDialog1.ShowDialog();
            if (dr2 == System.Windows.Forms.DialogResult.OK)
            {
                foreach (String file in openFileDialog1.FileNames)
                {
                    string name = file;
                    graphNames.Add(name);

                }
            }

            pictureBox1.ImageLocation = graphNames[0];
            pictureBox2.ImageLocation = graphNames[1];
            pictureBox3.ImageLocation = graphNames[2];

        }

        private void calibrateToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Calibrate";
            System.Diagnostics.Process.Start("CMD.exe");
        }

        private void rToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Recording";
            System.Diagnostics.Process.Start("CMD.exe");
        }

        private void analyseToolStripMenuItem_Click(object sender, EventArgs e)
        {
            toolStripStatusLabel1.Text = "Analysing";
            System.Diagnostics.Process process = new System.Diagnostics.Process();
            System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
            startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
            startInfo.FileName = "CMD.exe";
            startInfo.Arguments = "/C C:\\Python27\\pythonw.exe C:\\Users\\Chun_\\EDP\\gait-lab\\detection\\detect.py";
            process.StartInfo = startInfo;
            process.Start();
        }

        private void Play_button_Click(object sender, EventArgs e)
        {
            videoDisplay.Ctlcontrols.play();
        }

        private void pause_button_Click(object sender, EventArgs e)
        {
            videoDisplay.Ctlcontrols.pause();
        }

        private void prev_button_Click(object sender, EventArgs e)
        {
            IWMPControls2 Ctlcontrols2 = (IWMPControls2)videoDisplay.Ctlcontrols;
            Ctlcontrols2.step(-1);
        }

        private void next_button_Click(object sender, EventArgs e)
        {
            IWMPControls2 Ctlcontrols2 = (IWMPControls2)videoDisplay.Ctlcontrols;
            Ctlcontrols2.step(1);
        }

        private void videoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[0];
            videoLabel.Text = "Video 1";
        }

        private void video2ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[1];
            videoLabel.Text = "Video 2";
        }

        private void video3ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[2];
            videoLabel.Text = "Video 3";
        }

        private void video4ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            videoDisplay.URL = videoNames[3];
            videoLabel.Text = "Video 4";
        }

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
