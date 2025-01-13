import streamlit as st
st.graphviz_chart("""
        digraph {
           "penanngung jawab
        parhan dan agung "-> "ketua pelaksana"
          "ketua pelaksana"-> "bendahara dan sekertaris","schedule"
          "schedule"->"keamanan"
          "bendahara dan sekertaris"->"logistik"
         "logistik"->"masak "
        "schedule"->"dokumentasi"
                          
            
        
            
        }
    """)