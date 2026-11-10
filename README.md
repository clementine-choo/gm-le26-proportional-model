# Greater Manchester's LE26 Prediction Model
This is a model that predicts the 2026 Local Elections results in Greater Manchester using a proportional model. It assumes that each party's votes will swing proportionally across Greater Manchester and predicts the number of councillors won by each party as a result. 

Each party received the following vote share in the 2024 Local Elections:
    Labour: 44.5%
    Conservative: 17.3%
    Lib Dem: 11.4%
    Green: 10.3%
    Reform: 2.1%
    Workers Party and Others: 14.1%

However, because Reform UK did not stand many candidates in the 2024 Local Elections, Ben Walker's ward-level projection of 2024 General Election results was used instead.  

The default value for the 2026 Local Elections are:
    Labour 0.65x
    Conservative: 0.8x
    Lib Dem: 1x
    Green: 2x
    Reform: 2x
    Workers Party and Others: 1.2x

Therefore the default vote shares are:
    Labour: 22.4%
    Conservative: 10.7%
    Lib Dem: 8.8%
    Green: 18.4%
    Reform: 29.9%
    Workers Party and Others: 9.8%

And the new councillor counts are:
    Labour: 145 -> 35
    Conservative: 17 -> 10
    Lib Dem: 21 -> 20
    Green: 5 -> 25
    Reform: 0 -> 96
    Workers Party and Others: 27 -> 29

By picking actual ratios from the 2026 Local Elections:
    Labour: 0.67
    Conservative: 0.75
    Lib Dem: 0.99
    Green: 2.32
    Reform: 2.05
    Workers Party and Others: 0.84

The model predicts the following results:
    Labour: 34 councillors
    Conservative: 7 councillors
    Lib Dem: 21 councillors
    Green: 31 councillors
    Reform: 106 councillors
    Workers Party and Others: 16

The actual results are:
    Labour: 34 councillors (+0)
    Conservative: 11 councillors (+4)
    Lib Dem: 19 councillors (-2)
    Green: 30 councillor (-1)
    Reform: 105 councillors (+1)
    Workers Party and Others: 15 councillors (-1)

This shows that proportional model is remarkably accurate at predicting ward-level results


