// -*- C++ -*-
// 
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// parasim
// (c) 1998-2019 all rights reserved
// 

#if !defined(ampcor_extension_metadata_h)
#define ampcor_extension_metadata_h


// place everything in my private namespace
namespace ampcor {
    namespace extension {

        // copyright note
        extern const char * const copyright__name__;
        extern const char * const copyright__doc__;
        PyObject * copyright(PyObject *, PyObject *);

        // version
        extern const char * const version__name__;
        extern const char * const version__doc__;
        PyObject * version(PyObject *, PyObject *);

    } // of namespace extension`
} // of namespace ampcor

#endif

// end of file
