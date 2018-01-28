#pragma once
#include <iostream>
#include <sstream>
#include <string>

namespace EDP_GUI {

	using namespace std;
	using namespace WMPLib;
	using namespace AxWMPLib;
	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

	/// <summary>
	/// Summary for MyForm
	/// </summary>
	public ref class MyForm : public System::Windows::Forms::Form
	{
	public:
		MyForm(void)
		{
			InitializeComponent();
			//
			//TODO: Add the constructor code here
			//
		}

	protected:
		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		~MyForm()
		{
			if (components)
			{
				delete components;
			}
		}
	private: System::Windows::Forms::TableLayoutPanel^  tableLayoutPanel1;
	private: System::Windows::Forms::FlowLayoutPanel^  flowLayoutPanel1;
	private: System::Windows::Forms::Button^  Load_button;
	private: System::Windows::Forms::Button^  Calibrate_button;
	private: System::Windows::Forms::Button^  Analyse_button;
	private: System::Windows::Forms::MenuStrip^  menuStrip1;
	private: System::Windows::Forms::ToolStripMenuItem^  VideoDM;
	private: System::Windows::Forms::ToolStripMenuItem^  Video1_button;
	private: System::Windows::Forms::ToolStripMenuItem^  Video2_button;
	private: System::Windows::Forms::ToolStripMenuItem^  Video3_button;
	private: System::Windows::Forms::ToolStripMenuItem^  Video4_button;
	private: System::Windows::Forms::ToolStripMenuItem^  Video5_button;
	private: System::Windows::Forms::StatusStrip^  statusStrip1;
	private: System::Windows::Forms::ToolStripStatusLabel^  StatusLabel;
	private: System::Windows::Forms::ToolStripProgressBar^  ProgressBar;
	private: System::Windows::Forms::Label^  VideoLabel;
	private: System::Windows::Forms::MenuStrip^  menuStrip2;
	private: System::Windows::Forms::ToolStripMenuItem^  GraphDM;

	private: System::Windows::Forms::Button^  Help_button;

	private: System::Windows::Forms::Button^  Record_Button;

	private: System::Windows::Forms::Label^  DataLabel;

	private: System::Windows::Forms::OpenFileDialog^  openFileDialog1;
	private: System::Windows::Forms::SaveFileDialog^  saveFileDialog1;
	private: System::Windows::Forms::FlowLayoutPanel^  flowLayoutPanel2;
	private: System::Windows::Forms::Button^  PrevFrame_button;
	private: System::Windows::Forms::Button^  NextFrame_button;
	private: System::Windows::Forms::Label^  ControlLabel;
	private: System::Windows::Forms::Button^  Play_button;
	private: System::Windows::Forms::Button^  Pause_button;
	private: System::Windows::Forms::ToolStripMenuItem^  trunkSwayToolStripMenuItem;
	private: AxWMPLib::AxWindowsMediaPlayer^  VideoDisplay;
	private: System::Windows::Forms::PictureBox^  pictureBox1;





	protected:

	private:
		/// <summary>
		/// Required designer variable.
		/// </summary>
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		void InitializeComponent(void)//Initialisation of components followed by their respective properties
		{
			System::ComponentModel::ComponentResourceManager^  resources = (gcnew System::ComponentModel::ComponentResourceManager(MyForm::typeid));
			this->tableLayoutPanel1 = (gcnew System::Windows::Forms::TableLayoutPanel());
			this->flowLayoutPanel1 = (gcnew System::Windows::Forms::FlowLayoutPanel());
			this->Load_button = (gcnew System::Windows::Forms::Button());
			this->Calibrate_button = (gcnew System::Windows::Forms::Button());
			this->Record_Button = (gcnew System::Windows::Forms::Button());
			this->Analyse_button = (gcnew System::Windows::Forms::Button());
			this->menuStrip2 = (gcnew System::Windows::Forms::MenuStrip());
			this->GraphDM = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->trunkSwayToolStripMenuItem = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->menuStrip1 = (gcnew System::Windows::Forms::MenuStrip());
			this->VideoDM = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->Video1_button = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->Video2_button = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->Video3_button = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->Video4_button = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->Video5_button = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->Help_button = (gcnew System::Windows::Forms::Button());
			this->statusStrip1 = (gcnew System::Windows::Forms::StatusStrip());
			this->StatusLabel = (gcnew System::Windows::Forms::ToolStripStatusLabel());
			this->ProgressBar = (gcnew System::Windows::Forms::ToolStripProgressBar());
			this->VideoLabel = (gcnew System::Windows::Forms::Label());
			this->DataLabel = (gcnew System::Windows::Forms::Label());
			this->flowLayoutPanel2 = (gcnew System::Windows::Forms::FlowLayoutPanel());
			this->ControlLabel = (gcnew System::Windows::Forms::Label());
			this->Play_button = (gcnew System::Windows::Forms::Button());
			this->Pause_button = (gcnew System::Windows::Forms::Button());
			this->PrevFrame_button = (gcnew System::Windows::Forms::Button());
			this->NextFrame_button = (gcnew System::Windows::Forms::Button());
			this->VideoDisplay = (gcnew AxWMPLib::AxWindowsMediaPlayer());
			this->pictureBox1 = (gcnew System::Windows::Forms::PictureBox());
			this->openFileDialog1 = (gcnew System::Windows::Forms::OpenFileDialog());
			this->saveFileDialog1 = (gcnew System::Windows::Forms::SaveFileDialog());
			this->tableLayoutPanel1->SuspendLayout();
			this->flowLayoutPanel1->SuspendLayout();
			this->menuStrip2->SuspendLayout();
			this->menuStrip1->SuspendLayout();
			this->statusStrip1->SuspendLayout();
			this->flowLayoutPanel2->SuspendLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->VideoDisplay))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox1))->BeginInit();
			this->SuspendLayout();
			// 
			// tableLayoutPanel1
			// 
			this->tableLayoutPanel1->ColumnCount = 3;
			this->tableLayoutPanel1->ColumnStyles->Add((gcnew System::Windows::Forms::ColumnStyle(System::Windows::Forms::SizeType::Percent,
				34.27362F)));
			this->tableLayoutPanel1->ColumnStyles->Add((gcnew System::Windows::Forms::ColumnStyle(System::Windows::Forms::SizeType::Percent,
				65.72638F)));
			this->tableLayoutPanel1->ColumnStyles->Add((gcnew System::Windows::Forms::ColumnStyle(System::Windows::Forms::SizeType::Absolute,
				70)));
			this->tableLayoutPanel1->Controls->Add(this->flowLayoutPanel1, 0, 0);
			this->tableLayoutPanel1->Controls->Add(this->statusStrip1, 0, 5);
			this->tableLayoutPanel1->Controls->Add(this->VideoLabel, 1, 1);
			this->tableLayoutPanel1->Controls->Add(this->DataLabel, 0, 1);
			this->tableLayoutPanel1->Controls->Add(this->flowLayoutPanel2, 1, 4);
			this->tableLayoutPanel1->Controls->Add(this->VideoDisplay, 1, 2);
			this->tableLayoutPanel1->Controls->Add(this->pictureBox1, 0, 2);
			this->tableLayoutPanel1->Dock = System::Windows::Forms::DockStyle::Fill;
			this->tableLayoutPanel1->Location = System::Drawing::Point(0, 0);
			this->tableLayoutPanel1->Name = L"tableLayoutPanel1";
			this->tableLayoutPanel1->RowCount = 6;
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 37)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 24)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 232)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Percent, 100)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 35)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 37)));
			this->tableLayoutPanel1->Size = System::Drawing::Size(1301, 682);
			this->tableLayoutPanel1->TabIndex = 0;
			this->tableLayoutPanel1->Paint += gcnew System::Windows::Forms::PaintEventHandler(this, &MyForm::tableLayoutPanel1_Paint);
			// 
			// flowLayoutPanel1
			// 
			this->tableLayoutPanel1->SetColumnSpan(this->flowLayoutPanel1, 2);
			this->flowLayoutPanel1->Controls->Add(this->Load_button);
			this->flowLayoutPanel1->Controls->Add(this->Calibrate_button);
			this->flowLayoutPanel1->Controls->Add(this->Record_Button);
			this->flowLayoutPanel1->Controls->Add(this->Analyse_button);
			this->flowLayoutPanel1->Controls->Add(this->menuStrip2);
			this->flowLayoutPanel1->Controls->Add(this->menuStrip1);
			this->flowLayoutPanel1->Controls->Add(this->Help_button);
			this->flowLayoutPanel1->Dock = System::Windows::Forms::DockStyle::Fill;
			this->flowLayoutPanel1->Location = System::Drawing::Point(3, 3);
			this->flowLayoutPanel1->Name = L"flowLayoutPanel1";
			this->flowLayoutPanel1->Size = System::Drawing::Size(1224, 31);
			this->flowLayoutPanel1->TabIndex = 3;
			// 
			// Load_button
			// 
			this->Load_button->Dock = System::Windows::Forms::DockStyle::Top;
			this->Load_button->Location = System::Drawing::Point(3, 3);
			this->Load_button->Name = L"Load_button";
			this->Load_button->Size = System::Drawing::Size(75, 25);
			this->Load_button->TabIndex = 0;
			this->Load_button->Text = L"Load";
			this->Load_button->UseVisualStyleBackColor = true;
			this->Load_button->Click += gcnew System::EventHandler(this, &MyForm::Load_button_Click);
			// 
			// Calibrate_button
			// 
			this->Calibrate_button->Dock = System::Windows::Forms::DockStyle::Top;
			this->Calibrate_button->Location = System::Drawing::Point(84, 3);
			this->Calibrate_button->Name = L"Calibrate_button";
			this->Calibrate_button->Size = System::Drawing::Size(75, 25);
			this->Calibrate_button->TabIndex = 2;
			this->Calibrate_button->Text = L"Calibrate";
			this->Calibrate_button->UseVisualStyleBackColor = true;
			this->Calibrate_button->Click += gcnew System::EventHandler(this, &MyForm::Calibrate_button_Click);
			// 
			// Record_Button
			// 
			this->Record_Button->Location = System::Drawing::Point(165, 3);
			this->Record_Button->Name = L"Record_Button";
			this->Record_Button->Size = System::Drawing::Size(75, 23);
			this->Record_Button->TabIndex = 7;
			this->Record_Button->Text = L"Record";
			this->Record_Button->UseVisualStyleBackColor = true;
			this->Record_Button->Click += gcnew System::EventHandler(this, &MyForm::Record_Button_Click);
			// 
			// Analyse_button
			// 
			this->Analyse_button->Dock = System::Windows::Forms::DockStyle::Top;
			this->Analyse_button->Location = System::Drawing::Point(246, 3);
			this->Analyse_button->Name = L"Analyse_button";
			this->Analyse_button->Size = System::Drawing::Size(75, 25);
			this->Analyse_button->TabIndex = 3;
			this->Analyse_button->Text = L"Analyse";
			this->Analyse_button->UseVisualStyleBackColor = true;
			this->Analyse_button->Click += gcnew System::EventHandler(this, &MyForm::Analyse_button_Click);
			// 
			// menuStrip2
			// 
			this->menuStrip2->ImageScalingSize = System::Drawing::Size(20, 20);
			this->menuStrip2->Items->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(1) { this->GraphDM });
			this->menuStrip2->Location = System::Drawing::Point(324, 0);
			this->menuStrip2->Name = L"menuStrip2";
			this->menuStrip2->Size = System::Drawing::Size(75, 28);
			this->menuStrip2->TabIndex = 5;
			this->menuStrip2->Text = L"menuStrip2";
			// 
			// GraphDM
			// 
			this->GraphDM->DropDownItems->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(1) { this->trunkSwayToolStripMenuItem });
			this->GraphDM->Name = L"GraphDM";
			this->GraphDM->Size = System::Drawing::Size(67, 24);
			this->GraphDM->Text = L"Graphs";
			// 
			// trunkSwayToolStripMenuItem
			// 
			this->trunkSwayToolStripMenuItem->Name = L"trunkSwayToolStripMenuItem";
			this->trunkSwayToolStripMenuItem->Size = System::Drawing::Size(155, 26);
			this->trunkSwayToolStripMenuItem->Text = L"Trunk sway";
			this->trunkSwayToolStripMenuItem->Click += gcnew System::EventHandler(this, &MyForm::trunkSwayToolStripMenuItem_Click);
			// 
			// menuStrip1
			// 
			this->menuStrip1->ImageScalingSize = System::Drawing::Size(20, 20);
			this->menuStrip1->Items->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(1) { this->VideoDM });
			this->menuStrip1->Location = System::Drawing::Point(399, 0);
			this->menuStrip1->Name = L"menuStrip1";
			this->menuStrip1->Size = System::Drawing::Size(68, 28);
			this->menuStrip1->TabIndex = 4;
			this->menuStrip1->Text = L"menuStrip1";
			// 
			// VideoDM
			// 
			this->VideoDM->BackColor = System::Drawing::SystemColors::Control;
			this->VideoDM->BackgroundImageLayout = System::Windows::Forms::ImageLayout::Center;
			this->VideoDM->DropDownItems->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(5) {
				this->Video1_button,
					this->Video2_button, this->Video3_button, this->Video4_button, this->Video5_button
			});
			this->VideoDM->Name = L"VideoDM";
			this->VideoDM->Size = System::Drawing::Size(60, 24);
			this->VideoDM->Text = L"Video";
			// 
			// Video1_button
			// 
			this->Video1_button->BackColor = System::Drawing::SystemColors::Control;
			this->Video1_button->Name = L"Video1_button";
			this->Video1_button->Size = System::Drawing::Size(135, 26);
			this->Video1_button->Text = L"Video 1";
			this->Video1_button->Click += gcnew System::EventHandler(this, &MyForm::Video1_button_Click);
			// 
			// Video2_button
			// 
			this->Video2_button->BackColor = System::Drawing::SystemColors::Control;
			this->Video2_button->Name = L"Video2_button";
			this->Video2_button->Size = System::Drawing::Size(135, 26);
			this->Video2_button->Text = L"Video 2";
			this->Video2_button->Click += gcnew System::EventHandler(this, &MyForm::Video2_button_Click);
			// 
			// Video3_button
			// 
			this->Video3_button->BackColor = System::Drawing::SystemColors::Control;
			this->Video3_button->Name = L"Video3_button";
			this->Video3_button->Size = System::Drawing::Size(135, 26);
			this->Video3_button->Text = L"Video 3";
			this->Video3_button->Click += gcnew System::EventHandler(this, &MyForm::Video3_button_Click);
			// 
			// Video4_button
			// 
			this->Video4_button->BackColor = System::Drawing::SystemColors::Control;
			this->Video4_button->Name = L"Video4_button";
			this->Video4_button->Size = System::Drawing::Size(135, 26);
			this->Video4_button->Text = L"Video 4";
			this->Video4_button->Click += gcnew System::EventHandler(this, &MyForm::Video4_button_Click);
			// 
			// Video5_button
			// 
			this->Video5_button->BackColor = System::Drawing::SystemColors::Control;
			this->Video5_button->Name = L"Video5_button";
			this->Video5_button->Size = System::Drawing::Size(135, 26);
			this->Video5_button->Text = L"Video 5";
			this->Video5_button->Click += gcnew System::EventHandler(this, &MyForm::Video5_button_Click);
			// 
			// Help_button
			// 
			this->Help_button->Dock = System::Windows::Forms::DockStyle::Right;
			this->Help_button->Location = System::Drawing::Point(470, 3);
			this->Help_button->Name = L"Help_button";
			this->Help_button->Size = System::Drawing::Size(75, 25);
			this->Help_button->TabIndex = 6;
			this->Help_button->Text = L"Help";
			this->Help_button->UseVisualStyleBackColor = true;
			this->Help_button->Click += gcnew System::EventHandler(this, &MyForm::Help_button_Click);
			// 
			// statusStrip1
			// 
			this->tableLayoutPanel1->SetColumnSpan(this->statusStrip1, 2);
			this->statusStrip1->ImageScalingSize = System::Drawing::Size(20, 20);
			this->statusStrip1->Items->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(2) { this->StatusLabel, this->ProgressBar });
			this->statusStrip1->Location = System::Drawing::Point(0, 657);
			this->statusStrip1->Name = L"statusStrip1";
			this->statusStrip1->Size = System::Drawing::Size(1230, 25);
			this->statusStrip1->TabIndex = 2;
			this->statusStrip1->Text = L"statusStrip1";
			// 
			// StatusLabel
			// 
			this->StatusLabel->Name = L"StatusLabel";
			this->StatusLabel->Size = System::Drawing::Size(49, 20);
			this->StatusLabel->Text = L"Status";
			// 
			// ProgressBar
			// 
			this->ProgressBar->Name = L"ProgressBar";
			this->ProgressBar->Size = System::Drawing::Size(100, 19);
			// 
			// VideoLabel
			// 
			this->VideoLabel->AutoSize = true;
			this->VideoLabel->Dock = System::Windows::Forms::DockStyle::Bottom;
			this->VideoLabel->Location = System::Drawing::Point(424, 44);
			this->VideoLabel->Name = L"VideoLabel";
			this->VideoLabel->Size = System::Drawing::Size(803, 17);
			this->VideoLabel->TabIndex = 4;
			this->VideoLabel->Text = L"Video #no";
			this->VideoLabel->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
			// 
			// DataLabel
			// 
			this->DataLabel->AutoSize = true;
			this->DataLabel->Dock = System::Windows::Forms::DockStyle::Bottom;
			this->DataLabel->Location = System::Drawing::Point(3, 44);
			this->DataLabel->Name = L"DataLabel";
			this->DataLabel->Size = System::Drawing::Size(415, 17);
			this->DataLabel->TabIndex = 9;
			this->DataLabel->Text = L"Data";
			this->DataLabel->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
			// 
			// flowLayoutPanel2
			// 
			this->flowLayoutPanel2->Controls->Add(this->ControlLabel);
			this->flowLayoutPanel2->Controls->Add(this->Play_button);
			this->flowLayoutPanel2->Controls->Add(this->Pause_button);
			this->flowLayoutPanel2->Controls->Add(this->PrevFrame_button);
			this->flowLayoutPanel2->Controls->Add(this->NextFrame_button);
			this->flowLayoutPanel2->Dock = System::Windows::Forms::DockStyle::Fill;
			this->flowLayoutPanel2->Location = System::Drawing::Point(424, 613);
			this->flowLayoutPanel2->Name = L"flowLayoutPanel2";
			this->flowLayoutPanel2->Size = System::Drawing::Size(803, 29);
			this->flowLayoutPanel2->TabIndex = 10;
			// 
			// ControlLabel
			// 
			this->ControlLabel->AutoSize = true;
			this->ControlLabel->Dock = System::Windows::Forms::DockStyle::Left;
			this->ControlLabel->Location = System::Drawing::Point(3, 0);
			this->ControlLabel->Name = L"ControlLabel";
			this->ControlLabel->Size = System::Drawing::Size(98, 29);
			this->ControlLabel->TabIndex = 2;
			this->ControlLabel->Text = L"Video controls";
			this->ControlLabel->TextAlign = System::Drawing::ContentAlignment::MiddleCenter;
			// 
			// Play_button
			// 
			this->Play_button->Dock = System::Windows::Forms::DockStyle::Left;
			this->Play_button->Location = System::Drawing::Point(107, 3);
			this->Play_button->Name = L"Play_button";
			this->Play_button->Size = System::Drawing::Size(75, 23);
			this->Play_button->TabIndex = 3;
			this->Play_button->Text = L"Play";
			this->Play_button->UseVisualStyleBackColor = true;
			this->Play_button->Click += gcnew System::EventHandler(this, &MyForm::Play_button_Click);
			// 
			// Pause_button
			// 
			this->Pause_button->Dock = System::Windows::Forms::DockStyle::Left;
			this->Pause_button->Location = System::Drawing::Point(188, 3);
			this->Pause_button->Name = L"Pause_button";
			this->Pause_button->Size = System::Drawing::Size(75, 23);
			this->Pause_button->TabIndex = 4;
			this->Pause_button->Text = L"Pause";
			this->Pause_button->UseVisualStyleBackColor = true;
			this->Pause_button->Click += gcnew System::EventHandler(this, &MyForm::Pause_button_Click);
			// 
			// PrevFrame_button
			// 
			this->PrevFrame_button->Dock = System::Windows::Forms::DockStyle::Left;
			this->PrevFrame_button->Location = System::Drawing::Point(269, 3);
			this->PrevFrame_button->Name = L"PrevFrame_button";
			this->PrevFrame_button->Size = System::Drawing::Size(75, 23);
			this->PrevFrame_button->TabIndex = 0;
			this->PrevFrame_button->Text = L"<<";
			this->PrevFrame_button->UseVisualStyleBackColor = true;
			this->PrevFrame_button->Click += gcnew System::EventHandler(this, &MyForm::PrevFrame_button_Click);
			// 
			// NextFrame_button
			// 
			this->NextFrame_button->Location = System::Drawing::Point(350, 3);
			this->NextFrame_button->Name = L"NextFrame_button";
			this->NextFrame_button->Size = System::Drawing::Size(75, 23);
			this->NextFrame_button->TabIndex = 1;
			this->NextFrame_button->Text = L">>";
			this->NextFrame_button->UseVisualStyleBackColor = true;
			this->NextFrame_button->Click += gcnew System::EventHandler(this, &MyForm::NextFrame_button_Click);
			// 
			// VideoDisplay
			// 
			this->VideoDisplay->Dock = System::Windows::Forms::DockStyle::Fill;
			this->VideoDisplay->Enabled = true;
			this->VideoDisplay->Location = System::Drawing::Point(424, 64);
			this->VideoDisplay->Name = L"VideoDisplay";
			this->VideoDisplay->OcxState = (cli::safe_cast<System::Windows::Forms::AxHost::State^>(resources->GetObject(L"VideoDisplay.OcxState")));
			this->tableLayoutPanel1->SetRowSpan(this->VideoDisplay, 2);
			this->VideoDisplay->Size = System::Drawing::Size(803, 543);
			this->VideoDisplay->TabIndex = 8;
			// 
			// pictureBox1
			// 
			this->pictureBox1->Dock = System::Windows::Forms::DockStyle::Fill;
			this->pictureBox1->Location = System::Drawing::Point(3, 64);
			this->pictureBox1->Name = L"pictureBox1";
			this->pictureBox1->Size = System::Drawing::Size(415, 226);
			this->pictureBox1->TabIndex = 11;
			this->pictureBox1->TabStop = false;
			// 
			// openFileDialog1
			// 
			this->openFileDialog1->FileName = L"openFileDialog1";
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 16);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(1301, 682);
			this->Controls->Add(this->tableLayoutPanel1);
			this->Name = L"MyForm";
			this->Text = L"Gait lab";
			this->Load += gcnew System::EventHandler(this, &MyForm::MyForm_Load);
			this->tableLayoutPanel1->ResumeLayout(false);
			this->tableLayoutPanel1->PerformLayout();
			this->flowLayoutPanel1->ResumeLayout(false);
			this->flowLayoutPanel1->PerformLayout();
			this->menuStrip2->ResumeLayout(false);
			this->menuStrip2->PerformLayout();
			this->menuStrip1->ResumeLayout(false);
			this->menuStrip1->PerformLayout();
			this->statusStrip1->ResumeLayout(false);
			this->statusStrip1->PerformLayout();
			this->flowLayoutPanel2->ResumeLayout(false);
			this->flowLayoutPanel2->PerformLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->VideoDisplay))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox1))->EndInit();
			this->ResumeLayout(false);

		}
#pragma endregion
	private: System::Void tableLayoutPanel1_Paint(System::Object^  sender, System::Windows::Forms::PaintEventArgs^  e) {
	}

	private: System::Void flowLayoutPanel1_Paint(System::Object^  sender, System::Windows::Forms::PaintEventArgs^  e) {
	}

	private: System::Void MyForm_Load(System::Object^  sender, System::EventArgs^  e) {
	}

	private: System::Void Load_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Loading";
		OpenFileDialog^ openFileDialog1 = gcnew OpenFileDialog;

		openFileDialog1->InitialDirectory = "c:\\";
		openFileDialog1->Filter = "Mp4 files (*.mp4)|*.mp4|All files (*.*)|*.*";
		openFileDialog1->FilterIndex = 2;
		openFileDialog1->RestoreDirectory = true;

		if (openFileDialog1->ShowDialog() == System::Windows::Forms::DialogResult::OK)
		{
			
		}
	}

	private: System::Void Calibrate_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Calibrating";
	}

	private: System::Void Record_Button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Recording";
		MessageBox::Show("Remember to make a new folder for each session");
		this->StatusLabel->Text = L"Saving";
		// Displays a SaveFileDialog so the user can save the Videos
		SaveFileDialog ^ saveFileDialog1 = gcnew SaveFileDialog();
		saveFileDialog1->Filter = "MP4 Video|*.mp4";
		saveFileDialog1->Title = "Save Videos";
		saveFileDialog1->ShowDialog();
		// If the file name is not an empty string, open it for saving.
		if (saveFileDialog1->FileName != "") {
		}
	}

	private: System::Void Analyse_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Analysing";
		this->StatusLabel->Text = L"Saving";
		// Displays a SaveFileDialog so the user can save the Gait data
		SaveFileDialog ^ saveFileDialog1 = gcnew SaveFileDialog();
		saveFileDialog1->Filter = "JPeg Image|*.jpg"; // Need to change the file
		saveFileDialog1->Title = "Save Data";
		saveFileDialog1->ShowDialog();
		// If the file name is not an empty string, open it for saving.
		if (saveFileDialog1->FileName != "") {
		}
	}

	private: System::Void Help_button_Click(System::Object^  sender, System::EventArgs^  e) {
		MessageBox::Show("Help\nThe following text explains the functions of this program.\n\n"
			"Load:\nIf you wish to load analysis data and recordings from a past session."
			"\n\nCalibrate:\nThis will calibrate the camera system. It is important to do this before recroding any footage."
			"\n\nRecord:\nThis will begin the recording of footage."
			"\n\nAnalyse:\nThis will begin the anaylsis of the footage and add the data to a database which will be displayed."
			"\n\nGraphs:\nThis is the graph drop down menu."
			"\n\nPlot Graph:\nThis is located in the graph menu and will plot specified data into graph."
			"\n\nSave Graph:\nThis is located in the graph menu and will save any graphs generated to a folder of choice."
			"\n\nLoad Graphs from a previous session"
			"\n\nVideo:\nThis is the video drop down menu, selecting any of the videos will display it on the screen."
			"\n\nPlay:\nThis will play the video."
			"\n\nPause:\nThis will pause the video."
			"\n\n<<:\nThis will go to the previous frame."
			"\n\n>>:\nThis will go to the next frame."
		);
	}

	private: System::Void Video1_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoLabel->Text = L"Video 1";
		this->VideoDisplay->URL = ".\\TestVideo\\Video1.mp4";
	}

	private: System::Void Video2_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoLabel->Text = L"Video 2";
		this->VideoDisplay->URL = ".\\TestVideo\\Video2.mp4";
	}

	private: System::Void Video3_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoLabel->Text = L"Video 3";
		this->VideoDisplay->URL = ".\\TestVideo\\Video3.mp4";
	}

	private: System::Void Video4_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoLabel->Text = L"Video 4";
		this->VideoDisplay->URL = ".\\TestVideo\\Video4.mp4";

	}

	private: System::Void Video5_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoLabel->Text = L"Video 5";
		this->VideoDisplay->URL = ".\\TestVideo\\Video5.mp4";
	}

	private: System::Void SaveGraphs_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Saving";
		// Displays a SaveFileDialog so the user can save the Graph
		SaveFileDialog ^ saveFileDialog1 = gcnew SaveFileDialog();
		saveFileDialog1->Filter = "JPeg Image|*.jpg";
		saveFileDialog1->Title = "Save a Graph";
		saveFileDialog1->ShowDialog();
		// If the file name is not an empty string, open it for saving.
		if (saveFileDialog1->FileName != "") {
		}
	}

	private: System::Void loadGraphsToolStripMenuItem_Click(System::Object^  sender, System::EventArgs^  e) {
		// Displays a OpenFileDialog so the user can save the Graph
		MessageBox::Show("Choose a session and load the Graph");
		OpenFileDialog ^ openFileDialog1 = gcnew OpenFileDialog();
		openFileDialog1->Filter = "JPEG Image|*.jpg";
		openFileDialog1->Title = "Load graph";
		openFileDialog1->ShowDialog();
		// If the file name is not an empty string, open it for saving.
		if (openFileDialog1->FileName != "") {
		}
	}

	private: System::Void Play_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoDisplay->Ctlcontrols->play();
	}

	private: System::Void Pause_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->VideoDisplay->Ctlcontrols->pause();
	}

	private: System::Void PrevFrame_button_Click(System::Object^  sender, System::EventArgs^  e) {
		//(static_cast<IWMPControls2>(VideoDisplay->Ctlcontrols).step(1));
	}

	private: System::Void NextFrame_button_Click(System::Object^  sender, System::EventArgs^  e) {
	}
	private: System::Void trunkSwayToolStripMenuItem_Click(System::Object^  sender, System::EventArgs^  e) {
	}
};
}