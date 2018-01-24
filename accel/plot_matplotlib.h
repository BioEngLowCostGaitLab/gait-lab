#ifndef PLOT_MATPLOTLIB_H
#define PLOT_MATPLOTLIB_H

#include <string>
#include "Python.h"

using namespace std;

//!
//! \brief C++ wrapper class for Python plotting library "matplotlib".
//!
//! Matplotlib is a Python lib that can be used to plot scientific data in various ways.\n
//! A description can be found here: http://matplotlib.org/users/pyplot_tutorial.html\n
//! \n
//! Properties can be given in the format: property1=...[, property2=...]. Properties and matplotlib in general are explained here:\n
//! - http://matplotlib.org/users/pyplot_tutorial.html\n
//! - http://matplotlib.org/users/text_props.html#text-properties\n
//! - https://bespokeblog.wordpress.com/2011/07/07/basic-data-plotting-with-matplotlib-part-2-lines-points-formatting\n
//!
//! In text fields, latex-style formulas can be used.\n
//! \n
//! To be able to use this library on Mac OS X, install the required Python components:\n
//! <b>sudo easy_install pip; sudo pip install matplotlib</b>
//! \warning Requires that Py_Initialize(); was already called earlier in the program
//! \bug Multiple use of Py_Initialize(); (before in SVG parser and now here) is very buggy causing some random data to be visible on the plot. It can be removed by the ugly workaround "PyRun_SimpleString("pltt.clf()");" at the top of the Python code used for this plot.
//! \author Luke Pfirti
//! \version 0.01b
class plot_matplotlib
{

private:

    void PyRun_SimpleStringStd(std::string somestring)
    {
        PyRun_SimpleString(somestring.c_str());
        if(_pythoncmd != "") { _pythoncmd +="\n"; }
        _pythoncmd+=somestring;
    }

    bool _autorange;
    std::string _pythoncmd;
    double _range_x1, _range_x2, _range_y1, _range_y2;  // Range of the plot


public:

    plot_matplotlib() // Constructor
    {
        // Initialize automatic range:
        _range_x1 = std::numeric_limits<double>::max();
        _range_x2 = -std::numeric_limits<double>::max();
        _range_y1 = std::numeric_limits<double>::max();
        _range_y2 = -std::numeric_limits<double>::max();

        _pythoncmd="";
        _autorange=true;

        // Python:
        //Py_Initialize(); // Might already have been called?
        //std::cout << "- PY: import\n";
        PyRun_SimpleStringStd("import matplotlib.pyplot as pltt");
        //std::cout << "- PY: import done\n";
        PyRun_SimpleStringStd("pltt.clf()"); // Required because from SVG importing some data is still in the plot...? BUG!
        //std::cout << "- PY: cleared\n";
        //std::cout << "py init\n";
    }

    ~plot_matplotlib() // Destructor
    {
        //Py_Finalize();
        //std::cout << "- Python plot command:\n";
        //std::cout << pythoncmd;
    }

    //! \brief Set the label on the X axis
    void set_xlabel(std::string xlabel, std::string properties="")
    {
        if(properties!="") { properties=", "+properties; }
        this->PyRun_SimpleStringStd("pltt.xlabel('"+xlabel+"'"+properties+")");
    }
    //! \brief Set the label on the Y axis
    void set_ylabel(std::string ylabel, std::string properties="")
    {
        if(properties!="") { properties=", "+properties; }
        this->PyRun_SimpleStringStd("pltt.ylabel('"+ylabel+"'"+properties+")");
    }
    //! \brief Set the X and Y range of the plot
    void set_xyrange(double x1, double x2, double y1, double y2)
    {
        _autorange=false;
        this->PyRun_SimpleStringStd("pltt.axis(["+std::to_string(x1)+", "+std::to_string(x2)+", "+std::to_string(y1)+", "+std::to_string(y2)+"])");
    }
    //! \brief Set the plot title
    void set_title(std::string title)
    {
        this->PyRun_SimpleStringStd("pltt.title('"+title+"')");
    }
    //! \brief Set the aspect ratio of the plot to equal (desired for plotting paths and path Segments)
    void set_equal_ascpectratio()
    {
        this->PyRun_SimpleStringStd("pltt.axes().set_aspect('equal')");
    }



    //! \brief Set a figure (required for using subplots)
    void figure(int fignumber)
    {
        this->PyRun_SimpleStringStd("pltt.figure("+std::to_string(fignumber)+")");
    }
    //! \brief Set a subplot number
    void subplot(int plotnumber)
    {
        this->PyRun_SimpleStringStd("pltt.subplot("+std::to_string(plotnumber)+")");
    }

    //! \brief Enable a legend
    void enable_legend()
    {
        this->PyRun_SimpleStringStd("pltt.legend()");
    }



    //! \brief Calculate the plot range dependent on the added data (all data visible + small border, better than built standard range)
    void set_range_auto()
    {
        double extendpercent = 0.04;
        double xrange = _range_x2-_range_x1;
        double yrange = _range_y2-_range_y1;
        if(xrange<0) { xrange=xrange*-1.0; }
        if(yrange<0) { yrange=yrange*-1.0; }
        set_xyrange(_range_x1-xrange*extendpercent, _range_x2+xrange*extendpercent, _range_y1-yrange*extendpercent, _range_y2+yrange*extendpercent);
    }



    //! \brief Run a custom command on the current plot object
    //!
    //! This command allows to execute a custom matplotlib command on pltt (which was created by: import matplotlib.pyplot as pltt) E.g. running myplot->run_customcommand("show()") would do the same thing as myplot->show(): It executes the Python command: "pltt.show()".
    void run_customcommand(std::string command)
    {
        PyRun_SimpleStringStd("pltt."+command);
    }



    //! \brief Finally show the plot window (interrupts program execution until plot window is closed)
    void show()
    {
        //if(autorange && !_autorange) { this->set_range_auto(); }
        //if(keepaspectratio) { this->set_equal_ascpectratio(); }
        PyRun_SimpleStringStd("pltt.show()");

    }




    //! \brief Add data to the plot (X/Y points and matplotlib properties, e.g. 'o' for points or no properties for points connected by lines)
    void add_somedata(const std::vector<double> * X, const std::vector<double> * Y, std::string properties="'o'")
    {
        // Plot Points:
        std::string xpoints = "";
        std::string ypoints = "";
        for(int i=0;i<X->size();i++)
        {
            // Add points
            if(i>0) { xpoints += ","; }
            xpoints += std::to_string(X->at(i));
            if(i>0) { ypoints += ","; }
            ypoints += std::to_string(Y->at(i));

            // Set auto range
            if(X->at(i)<_range_x1) { _range_x1=X->at(i);  }
            if(X->at(i)>_range_x2) { _range_x2=X->at(i);  }
            if(Y->at(i)<_range_y1) { _range_y1=Y->at(i);  }
            if(Y->at(i)>_range_y2) { _range_y2=Y->at(i);  }
        }

        // PyRun_SimpleString("pltt.plot([1,2,3,4], [1,4,9,16], 'ro')");
        if(properties != "") { properties = ", "+properties; }
        this->PyRun_SimpleStringStd("pltt.plot(["+xpoints+"], ["+ypoints+"]"+properties+")");
    }



};

#endif // PLOT_MATPLOTLIB_H

