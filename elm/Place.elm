port module Place exposing (main)

import Html exposing (Html)
import Json.Encode
import Experiment


port jsonData : (Json.Encode.Value -> msg) -> Sub msg


type alias Model =
    { experiment : Experiment.Model
    , currentView : View
    , version : Version
    }


type View
    = Main
    | NewView
    | Experiment Int
    | Database
    | Settings


type Msg
    = ExperimentMsg Experiment.Msg


main : Program Flags Model Msg
main =
    Html.programWithFlags
        { init =
            \flags ->
                update (ExperimentMsg Experiment.GetStatus) <|
                    Model Experiment.init NewView (Version 0 0 0)
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


type alias Version =
    { major : Int
    , minor : Int
    , revision : Int
    }


type alias Flags =
    { version : String }


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ExperimentMsg experimentMsg ->
            let
                ( experimentModel, experimentCmd ) =
                    Experiment.update experimentMsg model.experiment
            in
                ( { model | experiment = experimentModel }, Cmd.map ExperimentMsg experimentCmd )


view : Model -> Html Msg
view model =
    case model.currentView of
        Main ->
            Html.text "PLACE Main View"

        NewView ->
            Html.div []
                [ Html.map ExperimentMsg <| Experiment.view model.experiment ]

        Experiment number ->
            Html.text <| "PLACE Experiment " ++ toString number ++ " View"

        Database ->
            Html.text "PLACE Database View"

        Settings ->
            Html.text "PLACE Settings View"



--loaderView : Model -> Html Msg
--loaderView model =
--    Html.div []
--        [ Html.p [ Html.Attributes.class "loaderTitle" ] [ Html.text "PLACE is busy" ]
--        , Html.div [ Html.Attributes.class "loader" ] []
--        , Html.p [ Html.Attributes.class "progresstext" ] [ Html.text (toString model.status) ]
--        ]


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch [ jsonData (\value -> ExperimentMsg (Experiment.UpdatePlugins value)) ]