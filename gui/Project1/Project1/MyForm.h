#pragma once
#include <iostream>
#include <sstream>
#include <string>

namespace EDP_GUI {

	using namespace std;
	using namespace WMPLib;
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







	private: System::Windows::Forms::OpenFileDialog^  openFileDialog1;
	private: System::Windows::Forms::SaveFileDialog^  saveFileDialog1;
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
	private: System::Windows::Forms::ToolStripMenuItem^  PlotGraph_Button;


	private: System::Windows::Forms::Button^  Help_button;

	private: AxWMPLib::AxWindowsMediaPlayer^  VideoDisplay;
	private: System::Windows::Forms::Button^  Record_Button;
	private: System::Windows::Forms::ToolStripMenuItem^  SaveGraphs_button;
	private: System::Windows::Forms::Label^  DataLabel;



























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
		void InitializeComponent(void)
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
			this->PlotGraph_Button = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->SaveGraphs_button = (gcnew System::Windows::Forms::ToolStripMenuItem());
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
			this->VideoDisplay = (gcnew AxWMPLib::AxWindowsMediaPlayer());
			this->openFileDialog1 = (gcnew System::Windows::Forms::OpenFileDialog());
			this->saveFileDialog1 = (gcnew System::Windows::Forms::SaveFileDialog());
			this->DataLabel = (gcnew System::Windows::Forms::Label());
			this->tableLayoutPanel1->SuspendLayout();
			this->flowLayoutPanel1->SuspendLayout();
			this->menuStrip2->SuspendLayout();
			this->menuStrip1->SuspendLayout();
			this->statusStrip1->SuspendLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->VideoDisplay))->BeginInit();
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
				54)));
			this->tableLayoutPanel1->Controls->Add(this->flowLayoutPanel1, 0, 0);
			this->tableLayoutPanel1->Controls->Add(this->statusStrip1, 0, 3);
			this->tableLayoutPanel1->Controls->Add(this->VideoLabel, 1, 1);
			this->tableLayoutPanel1->Controls->Add(this->VideoDisplay, 1, 2);
			this->tableLayoutPanel1->Controls->Add(this->DataLabel, 0, 1);
			this->tableLayoutPanel1->Dock = System::Windows::Forms::DockStyle::Fill;
			this->tableLayoutPanel1->Location = System::Drawing::Point(0, 0);
			this->tableLayoutPanel1->Name = L"tableLayoutPanel1";
			this->tableLayoutPanel1->RowCount = 4;
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 37)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 24)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Percent, 100)));
			this->tableLayoutPanel1->RowStyles->Add((gcnew System::Windows::Forms::RowStyle(System::Windows::Forms::SizeType::Absolute, 37)));
			this->tableLayoutPanel1->Size = System::Drawing::Size(909, 589);
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
			this->flowLayoutPanel1->Size = System::Drawing::Size(848, 31);
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
			this->GraphDM->DropDownItems->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(2) {
				this->PlotGraph_Button,
					this->SaveGraphs_button
			});
			this->GraphDM->Name = L"GraphDM";
			this->GraphDM->Size = System::Drawing::Size(67, 24);
			this->GraphDM->Text = L"Graphs";
			// 
			// PlotGraph_Button
			// 
			this->PlotGraph_Button->Name = L"PlotGraph_Button";
			this->PlotGraph_Button->Size = System::Drawing::Size(181, 26);
			this->PlotGraph_Button->Text = L"Plot";
			this->PlotGraph_Button->Click += gcnew System::EventHandler(this, &MyForm::PlotGraph_Button_Click);
			// 
			// SaveGraphs_button
			// 
			this->SaveGraphs_button->Name = L"SaveGraphs_button";
			this->SaveGraphs_button->Size = System::Drawing::Size(181, 26);
			this->SaveGraphs_button->Text = L"Save Graphs";
			this->SaveGraphs_button->Click += gcnew System::EventHandler(this, &MyForm::SaveGraphs_button_Click);
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
			this->statusStrip1->Location = System::Drawing::Point(0, 564);
			this->statusStrip1->Name = L"statusStrip1";
			this->statusStrip1->Size = System::Drawing::Size(854, 25);
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
			this->VideoLabel->Location = System::Drawing::Point(296, 44);
			this->VideoLabel->Name = L"VideoLabel";
			this->VideoLabel->Size = System::Drawing::Size(555, 17);
			this->VideoLabel->TabIndex = 4;
			this->VideoLabel->Text = L"Video #no";
			this->VideoLabel->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
			// 
			// VideoDisplay
			// 
			this->VideoDisplay->Dock = System::Windows::Forms::DockStyle::Fill;
			this->VideoDisplay->Enabled = true;
			this->VideoDisplay->Location = System::Drawing::Point(296, 64);
			this->VideoDisplay->Name = L"VideoDisplay";
			this->VideoDisplay->OcxState = (cli::safe_cast<System::Windows::Forms::AxHost::State^>(resources->GetObject(L"VideoDisplay.OcxState")));
			this->VideoDisplay->Size = System::Drawing::Size(555, 485);
			this->VideoDisplay->TabIndex = 8;
			// 
			// openFileDialog1
			// 
			this->openFileDialog1->FileName = L"openFileDialog1";
			this->openFileDialog1->FileOk += gcnew System::ComponentModel::CancelEventHandler(this, &MyForm::openFileDialog1_FileOk);
			// 
			// DataLabel
			// 
			this->DataLabel->AutoSize = true;
			this->DataLabel->Dock = System::Windows::Forms::DockStyle::Bottom;
			this->DataLabel->Location = System::Drawing::Point(3, 44);
			this->DataLabel->Name = L"DataLabel";
			this->DataLabel->Size = System::Drawing::Size(287, 17);
			this->DataLabel->TabIndex = 9;
			this->DataLabel->Text = L"Data";
			this->DataLabel->TextAlign = System::Drawing::ContentAlignment::MiddleLeft;
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 16);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(909, 589);
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
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->VideoDisplay))->EndInit();
			this->ResumeLayout(false);

		}
#pragma endregion
	private: System::Void tableLayoutPanel1_Paint(System::Object^  sender, System::Windows::Forms::PaintEventArgs^  e) {
	}
	private: System::Void flowLayoutPanel1_Paint(System::Object^  sender, System::Windows::Forms::PaintEventArgs^  e) {
	}
	private: System::Void MyForm_Load(System::Object^  sender, System::EventArgs^  e) {
	}
	private: System::Void openFileDialog1_FileOk(System::Object^  sender, System::ComponentModel::CancelEventArgs^  e) {
	}
	private: System::Void Load_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Loading";
	}
	private: System::Void Calibrate_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Calibrating";
	}
	private: System::Void Record_Button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Recording";
		stringstream videostream;
		SaveFileDialog^ saveFileDialog1 = gcnew SaveFileDialog;
		saveFileDialog1->Filter = "Video Files (*.mp4)|*.mp4|All files (*.*)|*.*";
		saveFileDialog1->FilterIndex = 2;
		saveFileDialog1->RestoreDirectory = true;
		if (saveFileDialog1->ShowDialog() == ::DialogResult::OK) {
			if ((videostream == saveFileDialog1->OpenFile()) != nullptr) {
				videostream->Clode();
			}
		}

	}
	private: System::Void Analyse_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Analysing";
	}
	private: System::Void Help_button_Click(System::Object^  sender, System::EventArgs^  e) {
		MessageBox::Show("Help\nThe following text explains the functions of this program.\n\n"
						 "Load:\nThis will ask you for a folder of data to load into the program."
						 "\n\nCalibrate:\nThis will calibrate the camera system. It is important to do this before recroding any footage."
						 "\n\nRecord:\nThis will begin the recording of footage."
						 "\n\nAnalyse:\This will begin the anaylsis of the footage and add the data to a database which will be displayed."
						 "\n\nGraphs:\nThis is the graph drop down menu."
						 "\n\nPlot Graph:\nThis is located in the graph menu and will plot specified data into graph."
						 "\n\nSave Graph:\nThis is located in the graph menu and will save any graphs generated to a folder of choice."
						 "\n\nVideo:\nThis is the video drop down menu, selecting any of the videos will display it on the screen."
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
	private: System::Void PlotGraph_Button_Click(System::Object^  sender, System::EventArgs^  e) {
	}
	private: System::Void SaveGraphs_button_Click(System::Object^  sender, System::EventArgs^  e) {
		this->StatusLabel->Text = L"Saving";
	}
};
}
