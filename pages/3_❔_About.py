import streamlit as st

st.markdown(
    """
    # About ASTRA
    Advanced Space Technology Roadmap Architecture (ASTRA) is a collaborative project between MIT and NASA to meet the following six objectives:
    1. **Map** the NASA technology portfolio to ongoing, planned and potential future missions using a systems approach compatible with NASA’s technology taxonomy (TX01-TX17)
    2. **Quantify** the mission targets achievable as a function of technological figures of merit including sensitivity analysis enabled by integrated modeling and parametric simulation
    3. **Technology** valuation and ranking of the existing technology portfolio (both centrally and in MDs) using TechPort, SMEs and the mission net-present-value (MNPV) concept
    4. **Portfolio** Construction by applying a TRL-risk-adapted Markowitz portfolio approach which generates a range of non-dominated space technology investment portfolios
    5. **Demonstrate** the usefulness of the ASTRA methodology by applying it to at least one case study from each MD and prototyping how its outputs could be integrated with and shown in NASA’s environment and tools such as TechPort
    6. **Disseminate** the importance of rigorous technology portfolio investment management using a combination of in-person workshops and online education classes
    # People
"""
)

profiles="""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
        <div class="card m-2" style="width: 15rem;">
            <img class="p-3 card-img-top rounded-circle" src="../static/images/person-icon.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Olivier L. de Weck</h5>
              <p class="card-text"><i>Professor</i>: </p>
            </div>
        </div>
        <div class="card m-2" style="width: 15rem;">
            <img class="p-3 card-img-top rounded-circle" src="../static/images/person-icon.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Afreen Siddiqi</h5>
              <p class="card-text"><i>Research Scientist</i>: </p>
            </div>
        </div>
        <div class="card m-2" style="width: 15rem;">
            <img class="p-3 card-img-top rounded-circle" src="../static/images/person-icon.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Julia Milton</h5>
              <p class="card-text"><i>PhD Candidate</i>: </p>
            </div>
        </div>
        <div class="card m-2" style="width: 15rem;">
            <img class="p-3 card-img-top rounded-circle" src="../static/images/person-icon.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Alex Koenig</h5>
              <p class="card-text"><i>SM</i>: </p>
            </div>
        </div>
        <div class="card m-2" style="width: 15rem;">
            <img class="p-3 card-img-top rounded-circle" src="../static/images/person-icon.jpg" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Roderick Huang</h5>
              <p class="card-text"><i>UROP</i>: </p>
            </div>
        </div>
    """
    
st.markdown(profiles, unsafe_allow_html= True)