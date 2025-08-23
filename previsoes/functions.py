def _split_features(features_string):
  if isinstance(features_string, str):
    return [feature.strip() for feature in features_string.split(',')]
  return []

def preprocess_new_data(
        entry_data,
        te_encoder,
        le_encoder,
        mlb,
        scaler
):
    """
    Preprocessa os dados de entrada de [entry_data] para o formato
    padronizado para o modelo na etapa de treino

    Args:
        entry_data: Dicionario contendo os dados brutos do carro da entrada do usuário.
                    Exemplo: {'Car Make': 'Toyota', 'Car Model': 'Camry', 'Year': 2020,
                            'Mileage': 30000, 'Fuel Type': 'Gasoline', 'Color': 'Black',
                            'Transmission': 'Automatic', 'Options/Features': 'Heated Seats, GPS',
                            'Condition': 'Used', 'Accident': 'No'}

    Retona:
        Um DataFrame com as features tratadas, pronto para ser submetido ao Modelo
    """
    from pandas import DataFrame, concat

    df_cols = [
        'Car Model', 'Year', 'Mileage', 'Fuel Type', 'Color',
        'Transmission', 'Options/Features', 'Accident'
    ]
    best_features = [
        'Car Model_Encoded',
        'Feature_Navigation',
        'Mileage',
        'Accident_Encoded',
        'Year'
    ] # 5 melhores Features selecionadas no treino do modelo
    new_car_df = DataFrame([{col: entry_data.get(col, None) for col in df_cols}])
    numerical_cols = ['Car Model_Encoded', 'Year', 'Mileage']

    new_car_df['Car Model_Encoded'] = te_encoder.transform(new_car_df['Car Model'])
    new_car_df['Accident_Encoded'] = le_encoder.transform(new_car_df['Accident'])

    new_car_df['Options/Features_list'] = new_car_df['Options/Features'].apply(_split_features)
    new_car_features_encoded = mlb.transform(new_car_df['Options/Features_list'])
    feature_column_names = [f'Feature_{c}' for c in mlb.classes_]
    new_car_features_encoded_df = DataFrame(new_car_features_encoded, columns=feature_column_names, index=new_car_df.index)

    cols_to_drop_after_mlb = ['Options/Features', 'Options/Features_list']
    new_car_df = concat([new_car_df.drop(cols_to_drop_after_mlb, axis=1, errors='ignore'), new_car_features_encoded_df], axis=1)
    
    new_car_df[numerical_cols] = scaler.transform(new_car_df[numerical_cols])

    return new_car_df[best_features]


def predict_price(data: dict, model) -> float:
    """
    Predicts the price of a new car using the loaded pipeline.

    Args:
        new_car_data: A dictionary containing the raw features of a new car.

    Returns:
        The predicted price as a float, or None if prediction fails.
    """
    try:
        prediction = model.predict(data)[0]
        return float(prediction)
    except Exception as e:
        print(f"Error during prediction: {e}")
        # In a real backend, log the error
        return None
