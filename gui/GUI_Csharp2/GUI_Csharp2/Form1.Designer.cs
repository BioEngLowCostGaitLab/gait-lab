//Added the same libs
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUI_Csharp2
{
    partial class GUI_Csharp
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        /// 

        public void Intialise(List<string> list, int i)// Initialise the lists with a desired size
        {
            for(int j = 0; j < i; j++)
            {
                list.Add("");
            }
        }

        public void Fill(List<string> list)// Fill the arrays with blanks
        {
            for (int i = 0; i < list.Count; i++)
            {
                list[i] = "";
            }
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(GUI_Csharp));
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.UI_menu = new System.Windows.Forms.FlowLayoutPanel();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.loadMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.calibrateMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.recordMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.analyseMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.graphsMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.printMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.videosMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.video1ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.video2ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.video3ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.video4ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.helpMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.loadHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.calibrateHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.recordHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.analyseHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.graphHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.printHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.videoHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.videoControlsHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.playHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.pauseHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.prevHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.nrxtHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.videoControls = new System.Windows.Forms.FlowLayoutPanel();
            this.playButton = new System.Windows.Forms.Button();
            this.pauseButton = new System.Windows.Forms.Button();
            this.prevButton = new System.Windows.Forms.Button();
            this.nextButton = new System.Windows.Forms.Button();
            this.videoDisplay = new AxWMPLib.AxWindowsMediaPlayer();
            this.infoLabel = new System.Windows.Forms.Label();
            this.tableLayoutPanel4 = new System.Windows.Forms.TableLayoutPanel();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.leftKnee = new System.Windows.Forms.Label();
            this.rightKnee = new System.Windows.Forms.Label();
            this.joints = new System.Windows.Forms.Label();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.toolStripStatusLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripProgressBar1 = new System.Windows.Forms.ToolStripProgressBar();
            this.graphLabel = new System.Windows.Forms.Label();
            this.videoLabel = new System.Windows.Forms.Label();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.pictureBox2 = new System.Windows.Forms.PictureBox();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.tableLayoutPanel1.SuspendLayout();
            this.UI_menu.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.videoControls.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.videoDisplay)).BeginInit();
            this.tableLayoutPanel4.SuspendLayout();
            this.statusStrip1.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 3;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.2992F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 65.69019F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 1.010618F));
            this.tableLayoutPanel1.Controls.Add(this.UI_menu, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 2);
            this.tableLayoutPanel1.Controls.Add(this.statusStrip1, 0, 3);
            this.tableLayoutPanel1.Controls.Add(this.graphLabel, 1, 1);
            this.tableLayoutPanel1.Controls.Add(this.videoLabel, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel3, 1, 2);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 4;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 38F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 3.113553F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 96.88644F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 30F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(1099, 630);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // UI_menu
            // 
            this.UI_menu.BackColor = System.Drawing.SystemColors.MenuBar;
            this.tableLayoutPanel1.SetColumnSpan(this.UI_menu, 3);
            this.UI_menu.Controls.Add(this.menuStrip1);
            this.UI_menu.Dock = System.Windows.Forms.DockStyle.Fill;
            this.UI_menu.Location = new System.Drawing.Point(3, 2);
            this.UI_menu.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.UI_menu.Name = "UI_menu";
            this.UI_menu.Size = new System.Drawing.Size(1093, 34);
            this.UI_menu.TabIndex = 1;
            // 
            // menuStrip1
            // 
            this.menuStrip1.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.loadMenu,
            this.calibrateMenu,
            this.recordMenu,
            this.analyseMenu,
            this.graphsMenu,
            this.videosMenu,
            this.helpMenu});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Padding = new System.Windows.Forms.Padding(5, 2, 0, 2);
            this.menuStrip1.Size = new System.Drawing.Size(468, 28);
            this.menuStrip1.TabIndex = 4;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // loadMenu
            // 
            this.loadMenu.BackColor = System.Drawing.SystemColors.Control;
            this.loadMenu.Name = "loadMenu";
            this.loadMenu.Size = new System.Drawing.Size(54, 24);
            this.loadMenu.Text = "Load";
            this.loadMenu.Click += new System.EventHandler(this.loadToolStripMenuItem_Click);
            // 
            // calibrateMenu
            // 
            this.calibrateMenu.Name = "calibrateMenu";
            this.calibrateMenu.Size = new System.Drawing.Size(81, 24);
            this.calibrateMenu.Text = "Calibrate";
            this.calibrateMenu.Click += new System.EventHandler(this.calibrateToolStripMenuItem_Click);
            // 
            // recordMenu
            // 
            this.recordMenu.Name = "recordMenu";
            this.recordMenu.Size = new System.Drawing.Size(68, 24);
            this.recordMenu.Text = "Record";
            this.recordMenu.Click += new System.EventHandler(this.rToolStripMenuItem_Click);
            // 
            // analyseMenu
            // 
            this.analyseMenu.Name = "analyseMenu";
            this.analyseMenu.Size = new System.Drawing.Size(72, 24);
            this.analyseMenu.Text = "Analyse";
            this.analyseMenu.Click += new System.EventHandler(this.analyseToolStripMenuItem_Click);
            // 
            // graphsMenu
            // 
            this.graphsMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.printMenu});
            this.graphsMenu.Name = "graphsMenu";
            this.graphsMenu.Size = new System.Drawing.Size(67, 24);
            this.graphsMenu.Text = "Graphs";
            // 
            // printMenu
            // 
            this.printMenu.Name = "printMenu";
            this.printMenu.Size = new System.Drawing.Size(114, 26);
            this.printMenu.Text = "Print";
            this.printMenu.Click += new System.EventHandler(this.printMenu_Click);
            // 
            // videosMenu
            // 
            this.videosMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.video1ToolStripMenuItem,
            this.video2ToolStripMenuItem,
            this.video3ToolStripMenuItem,
            this.video4ToolStripMenuItem});
            this.videosMenu.Name = "videosMenu";
            this.videosMenu.Size = new System.Drawing.Size(66, 24);
            this.videosMenu.Text = "Videos";
            // 
            // video1ToolStripMenuItem
            // 
            this.video1ToolStripMenuItem.Name = "video1ToolStripMenuItem";
            this.video1ToolStripMenuItem.Size = new System.Drawing.Size(135, 26);
            this.video1ToolStripMenuItem.Text = "Video 1";
            this.video1ToolStripMenuItem.Click += new System.EventHandler(this.videoToolStripMenuItem_Click);
            // 
            // video2ToolStripMenuItem
            // 
            this.video2ToolStripMenuItem.Name = "video2ToolStripMenuItem";
            this.video2ToolStripMenuItem.Size = new System.Drawing.Size(135, 26);
            this.video2ToolStripMenuItem.Text = "Video 2";
            this.video2ToolStripMenuItem.Click += new System.EventHandler(this.video2ToolStripMenuItem_Click);
            // 
            // video3ToolStripMenuItem
            // 
            this.video3ToolStripMenuItem.Name = "video3ToolStripMenuItem";
            this.video3ToolStripMenuItem.Size = new System.Drawing.Size(135, 26);
            this.video3ToolStripMenuItem.Text = "Video 3";
            this.video3ToolStripMenuItem.Click += new System.EventHandler(this.video3ToolStripMenuItem_Click);
            // 
            // video4ToolStripMenuItem
            // 
            this.video4ToolStripMenuItem.Name = "video4ToolStripMenuItem";
            this.video4ToolStripMenuItem.Size = new System.Drawing.Size(135, 26);
            this.video4ToolStripMenuItem.Text = "Video 4";
            this.video4ToolStripMenuItem.Click += new System.EventHandler(this.video4ToolStripMenuItem_Click);
            // 
            // helpMenu
            // 
            this.helpMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.loadHelp,
            this.calibrateHelp,
            this.recordHelp,
            this.analyseHelp,
            this.graphHelp,
            this.videoHelp,
            this.videoControlsHelp});
            this.helpMenu.Name = "helpMenu";
            this.helpMenu.Size = new System.Drawing.Size(53, 24);
            this.helpMenu.Text = "Help";
            // 
            // loadHelp
            // 
            this.loadHelp.Name = "loadHelp";
            this.loadHelp.Size = new System.Drawing.Size(182, 26);
            this.loadHelp.Text = "Load";
            this.loadHelp.Click += new System.EventHandler(this.loadToolStripMenuItem1_Click);
            // 
            // calibrateHelp
            // 
            this.calibrateHelp.Name = "calibrateHelp";
            this.calibrateHelp.Size = new System.Drawing.Size(182, 26);
            this.calibrateHelp.Text = "Calibrate";
            this.calibrateHelp.Click += new System.EventHandler(this.calibrateToolStripMenuItem1_Click);
            // 
            // recordHelp
            // 
            this.recordHelp.Name = "recordHelp";
            this.recordHelp.Size = new System.Drawing.Size(182, 26);
            this.recordHelp.Text = "Record";
            this.recordHelp.Click += new System.EventHandler(this.recordToolStripMenuItem_Click);
            // 
            // analyseHelp
            // 
            this.analyseHelp.Name = "analyseHelp";
            this.analyseHelp.Size = new System.Drawing.Size(182, 26);
            this.analyseHelp.Text = "Analyse";
            this.analyseHelp.Click += new System.EventHandler(this.analyseToolStripMenuItem1_Click);
            // 
            // graphHelp
            // 
            this.graphHelp.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.printHelp});
            this.graphHelp.Name = "graphHelp";
            this.graphHelp.Size = new System.Drawing.Size(182, 26);
            this.graphHelp.Text = "Graphs";
            // 
            // printHelp
            // 
            this.printHelp.Name = "printHelp";
            this.printHelp.Size = new System.Drawing.Size(114, 26);
            this.printHelp.Text = "Print";
            this.printHelp.Click += new System.EventHandler(this.printToolStripMenuItem1_Click);
            // 
            // videoHelp
            // 
            this.videoHelp.Name = "videoHelp";
            this.videoHelp.Size = new System.Drawing.Size(182, 26);
            this.videoHelp.Text = "Videos";
            this.videoHelp.Click += new System.EventHandler(this.videosToolStripMenuItem1_Click);
            // 
            // videoControlsHelp
            // 
            this.videoControlsHelp.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.playHelp,
            this.pauseHelp,
            this.prevHelp,
            this.nrxtHelp});
            this.videoControlsHelp.Name = "videoControlsHelp";
            this.videoControlsHelp.Size = new System.Drawing.Size(182, 26);
            this.videoControlsHelp.Text = "Video Controls";
            // 
            // playHelp
            // 
            this.playHelp.Name = "playHelp";
            this.playHelp.Size = new System.Drawing.Size(121, 26);
            this.playHelp.Text = "Play";
            this.playHelp.Click += new System.EventHandler(this.playToolStripMenuItem_Click);
            // 
            // pauseHelp
            // 
            this.pauseHelp.Name = "pauseHelp";
            this.pauseHelp.Size = new System.Drawing.Size(121, 26);
            this.pauseHelp.Text = "Pause";
            this.pauseHelp.Click += new System.EventHandler(this.pauseToolStripMenuItem_Click);
            // 
            // prevHelp
            // 
            this.prevHelp.Name = "prevHelp";
            this.prevHelp.Size = new System.Drawing.Size(121, 26);
            this.prevHelp.Text = "<<";
            this.prevHelp.Click += new System.EventHandler(this.toolStripMenuItem2_Click);
            // 
            // nrxtHelp
            // 
            this.nrxtHelp.Name = "nrxtHelp";
            this.nrxtHelp.Size = new System.Drawing.Size(121, 26);
            this.nrxtHelp.Text = ">>";
            this.nrxtHelp.Click += new System.EventHandler(this.toolStripMenuItem3_Click);
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.BackColor = System.Drawing.SystemColors.Window;
            this.tableLayoutPanel2.ColumnCount = 1;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.Controls.Add(this.videoControls, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.videoDisplay, 0, 0);
            this.tableLayoutPanel2.Controls.Add(this.infoLabel, 0, 2);
            this.tableLayoutPanel2.Controls.Add(this.tableLayoutPanel4, 0, 3);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 57);
            this.tableLayoutPanel2.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 4;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 48.11083F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 37F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 51.88917F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(359, 540);
            this.tableLayoutPanel2.TabIndex = 4;
            // 
            // videoControls
            // 
            this.videoControls.BackColor = System.Drawing.SystemColors.MenuBar;
            this.videoControls.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.videoControls.Controls.Add(this.playButton);
            this.videoControls.Controls.Add(this.pauseButton);
            this.videoControls.Controls.Add(this.prevButton);
            this.videoControls.Controls.Add(this.nextButton);
            this.videoControls.Dock = System.Windows.Forms.DockStyle.Fill;
            this.videoControls.Location = new System.Drawing.Point(3, 231);
            this.videoControls.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.videoControls.Name = "videoControls";
            this.videoControls.Size = new System.Drawing.Size(353, 33);
            this.videoControls.TabIndex = 8;
            // 
            // playButton
            // 
            this.playButton.Location = new System.Drawing.Point(3, 2);
            this.playButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.playButton.Name = "playButton";
            this.playButton.Size = new System.Drawing.Size(75, 23);
            this.playButton.TabIndex = 0;
            this.playButton.Text = "Play";
            this.playButton.UseVisualStyleBackColor = true;
            this.playButton.Click += new System.EventHandler(this.Play_button_Click);
            // 
            // pauseButton
            // 
            this.pauseButton.Location = new System.Drawing.Point(84, 2);
            this.pauseButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.pauseButton.Name = "pauseButton";
            this.pauseButton.Size = new System.Drawing.Size(75, 23);
            this.pauseButton.TabIndex = 1;
            this.pauseButton.Text = "Pause";
            this.pauseButton.UseVisualStyleBackColor = true;
            this.pauseButton.Click += new System.EventHandler(this.pause_button_Click);
            // 
            // prevButton
            // 
            this.prevButton.Location = new System.Drawing.Point(165, 2);
            this.prevButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.prevButton.Name = "prevButton";
            this.prevButton.Size = new System.Drawing.Size(75, 23);
            this.prevButton.TabIndex = 2;
            this.prevButton.Text = "<<";
            this.prevButton.UseVisualStyleBackColor = true;
            this.prevButton.Click += new System.EventHandler(this.prev_button_Click);
            // 
            // nextButton
            // 
            this.nextButton.Location = new System.Drawing.Point(246, 2);
            this.nextButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.nextButton.Name = "nextButton";
            this.nextButton.Size = new System.Drawing.Size(75, 23);
            this.nextButton.TabIndex = 3;
            this.nextButton.Text = ">>";
            this.nextButton.UseVisualStyleBackColor = true;
            this.nextButton.Click += new System.EventHandler(this.next_button_Click);
            // 
            // videoDisplay
            // 
            this.videoDisplay.Dock = System.Windows.Forms.DockStyle.Fill;
            this.videoDisplay.Enabled = true;
            this.videoDisplay.Location = new System.Drawing.Point(3, 2);
            this.videoDisplay.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.videoDisplay.Name = "videoDisplay";
            this.videoDisplay.OcxState = ((System.Windows.Forms.AxHost.State)(resources.GetObject("videoDisplay.OcxState")));
            this.videoDisplay.Size = new System.Drawing.Size(353, 225);
            this.videoDisplay.TabIndex = 7;
            // 
            // infoLabel
            // 
            this.infoLabel.AutoSize = true;
            this.infoLabel.Location = new System.Drawing.Point(3, 266);
            this.infoLabel.Name = "infoLabel";
            this.infoLabel.Size = new System.Drawing.Size(60, 17);
            this.infoLabel.TabIndex = 4;
            this.infoLabel.Text = "Anaylsis";
            // 
            // tableLayoutPanel4
            // 
            this.tableLayoutPanel4.CellBorderStyle = System.Windows.Forms.TableLayoutPanelCellBorderStyle.Inset;
            this.tableLayoutPanel4.ColumnCount = 2;
            this.tableLayoutPanel4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 29.4686F));
            this.tableLayoutPanel4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 70.5314F));
            this.tableLayoutPanel4.Controls.Add(this.label4, 1, 2);
            this.tableLayoutPanel4.Controls.Add(this.label3, 1, 1);
            this.tableLayoutPanel4.Controls.Add(this.label1, 1, 0);
            this.tableLayoutPanel4.Controls.Add(this.leftKnee, 0, 2);
            this.tableLayoutPanel4.Controls.Add(this.rightKnee, 0, 1);
            this.tableLayoutPanel4.Controls.Add(this.joints, 0, 0);
            this.tableLayoutPanel4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel4.Location = new System.Drawing.Point(3, 293);
            this.tableLayoutPanel4.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.tableLayoutPanel4.Name = "tableLayoutPanel4";
            this.tableLayoutPanel4.RowCount = 3;
            this.tableLayoutPanel4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel4.Size = new System.Drawing.Size(353, 245);
            this.tableLayoutPanel4.TabIndex = 5;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label4.Location = new System.Drawing.Point(109, 164);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(239, 79);
            this.label4.TabIndex = 12;
            this.label4.Text = "Information";
            this.label4.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label3.Location = new System.Drawing.Point(109, 83);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(239, 79);
            this.label3.TabIndex = 11;
            this.label3.Text = "Information";
            this.label3.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label1.Location = new System.Drawing.Point(109, 2);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(239, 79);
            this.label1.TabIndex = 9;
            this.label1.Text = "Angle";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // leftKnee
            // 
            this.leftKnee.AutoSize = true;
            this.leftKnee.Dock = System.Windows.Forms.DockStyle.Fill;
            this.leftKnee.Location = new System.Drawing.Point(5, 164);
            this.leftKnee.Name = "leftKnee";
            this.leftKnee.Size = new System.Drawing.Size(96, 79);
            this.leftKnee.TabIndex = 6;
            this.leftKnee.Text = "Left Knee";
            this.leftKnee.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // rightKnee
            // 
            this.rightKnee.AutoSize = true;
            this.rightKnee.Dock = System.Windows.Forms.DockStyle.Fill;
            this.rightKnee.Location = new System.Drawing.Point(5, 83);
            this.rightKnee.Name = "rightKnee";
            this.rightKnee.Size = new System.Drawing.Size(96, 79);
            this.rightKnee.TabIndex = 4;
            this.rightKnee.Text = "Right Knee";
            this.rightKnee.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // joints
            // 
            this.joints.AutoSize = true;
            this.joints.Dock = System.Windows.Forms.DockStyle.Fill;
            this.joints.Location = new System.Drawing.Point(5, 2);
            this.joints.Name = "joints";
            this.joints.Size = new System.Drawing.Size(96, 79);
            this.joints.TabIndex = 1;
            this.joints.Text = "Joint";
            this.joints.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // statusStrip1
            // 
            this.tableLayoutPanel1.SetColumnSpan(this.statusStrip1, 3);
            this.statusStrip1.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripStatusLabel1,
            this.toolStripProgressBar1});
            this.statusStrip1.Location = new System.Drawing.Point(0, 601);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Padding = new System.Windows.Forms.Padding(1, 0, 13, 0);
            this.statusStrip1.Size = new System.Drawing.Size(1099, 29);
            this.statusStrip1.TabIndex = 6;
            this.statusStrip1.Text = "statusStrip1";
            // 
            // toolStripStatusLabel1
            // 
            this.toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            this.toolStripStatusLabel1.Size = new System.Drawing.Size(18, 24);
            this.toolStripStatusLabel1.Text = "#";
            // 
            // toolStripProgressBar1
            // 
            this.toolStripProgressBar1.Name = "toolStripProgressBar1";
            this.toolStripProgressBar1.Size = new System.Drawing.Size(100, 23);
            // 
            // graphLabel
            // 
            this.graphLabel.AutoSize = true;
            this.graphLabel.Location = new System.Drawing.Point(368, 38);
            this.graphLabel.Name = "graphLabel";
            this.graphLabel.Size = new System.Drawing.Size(55, 17);
            this.graphLabel.TabIndex = 3;
            this.graphLabel.Text = "Graphs";
            // 
            // videoLabel
            // 
            this.videoLabel.AutoSize = true;
            this.videoLabel.Location = new System.Drawing.Point(3, 38);
            this.videoLabel.Name = "videoLabel";
            this.videoLabel.Size = new System.Drawing.Size(56, 17);
            this.videoLabel.TabIndex = 2;
            this.videoLabel.Text = "Video #";
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.CellBorderStyle = System.Windows.Forms.TableLayoutPanelCellBorderStyle.Single;
            this.tableLayoutPanel3.ColumnCount = 1;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel3.Controls.Add(this.pictureBox2, 0, 1);
            this.tableLayoutPanel3.Controls.Add(this.pictureBox1, 0, 0);
            this.tableLayoutPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel3.Location = new System.Drawing.Point(369, 59);
            this.tableLayoutPanel3.Margin = new System.Windows.Forms.Padding(4);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 2;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(713, 536);
            this.tableLayoutPanel3.TabIndex = 7;
            // 
            // pictureBox2
            // 
            this.pictureBox2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pictureBox2.Location = new System.Drawing.Point(5, 272);
            this.pictureBox2.Margin = new System.Windows.Forms.Padding(4);
            this.pictureBox2.Name = "pictureBox2";
            this.pictureBox2.Size = new System.Drawing.Size(703, 259);
            this.pictureBox2.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox2.TabIndex = 1;
            this.pictureBox2.TabStop = false;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pictureBox1.Location = new System.Drawing.Point(5, 5);
            this.pictureBox1.Margin = new System.Windows.Forms.Padding(4);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(703, 258);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "Open Files";
            // 
            // GUI_Csharp
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(1099, 630);
            this.Controls.Add(this.tableLayoutPanel1);
            this.MainMenuStrip = this.menuStrip1;
            this.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.Name = "GUI_Csharp";
            this.Text = "GUI C#";
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.UI_menu.ResumeLayout(false);
            this.UI_menu.PerformLayout();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.PerformLayout();
            this.videoControls.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.videoDisplay)).EndInit();
            this.tableLayoutPanel4.ResumeLayout(false);
            this.tableLayoutPanel4.PerformLayout();
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.tableLayoutPanel3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.FlowLayoutPanel UI_menu;
        private System.Windows.Forms.Label graphLabel;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.Label videoLabel;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.Label infoLabel;
        private System.Windows.Forms.ToolStripMenuItem loadMenu;
        private System.Windows.Forms.ToolStripMenuItem calibrateMenu;
        private System.Windows.Forms.ToolStripMenuItem recordMenu;
        private System.Windows.Forms.ToolStripMenuItem analyseMenu;
        private System.Windows.Forms.ToolStripMenuItem graphsMenu;
        private System.Windows.Forms.ToolStripMenuItem videosMenu;
        private System.Windows.Forms.ToolStripMenuItem video1ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem video2ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem video3ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem video4ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem helpMenu;
        private System.Windows.Forms.ToolStripMenuItem loadHelp;
        private System.Windows.Forms.ToolStripMenuItem calibrateHelp;
        private System.Windows.Forms.ToolStripMenuItem recordHelp;
        private System.Windows.Forms.ToolStripMenuItem analyseHelp;
        private System.Windows.Forms.ToolStripMenuItem graphHelp;
        private System.Windows.Forms.ToolStripMenuItem videoHelp;
        private System.Windows.Forms.ToolStripMenuItem videoControlsHelp;
        private System.Windows.Forms.ToolStripMenuItem playHelp;
        private System.Windows.Forms.ToolStripMenuItem pauseHelp;
        private System.Windows.Forms.ToolStripMenuItem prevHelp;
        private System.Windows.Forms.ToolStripMenuItem nrxtHelp;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel1;
        private System.Windows.Forms.ToolStripProgressBar toolStripProgressBar1;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel4;
        private System.Windows.Forms.Label leftKnee;
        private System.Windows.Forms.Label rightKnee;
        private System.Windows.Forms.Label joints;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ToolTip toolTip1;
        private System.Windows.Forms.FlowLayoutPanel videoControls;
        private System.Windows.Forms.Button playButton;
        private System.Windows.Forms.Button pauseButton;
        private System.Windows.Forms.Button prevButton;
        private System.Windows.Forms.Button nextButton;
        private AxWMPLib.AxWindowsMediaPlayer videoDisplay;
        private System.Windows.Forms.ToolStripMenuItem printMenu;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private System.Windows.Forms.PictureBox pictureBox2;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.ToolStripMenuItem printHelp;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
    }
}

