import pandas as pd

def _split_features(features_string):
  if isinstance(features_string, str):
    return [feature.strip() for feature in features_string.split(',')]
  return []

def gerarPrevisao(car_data, model, te_encoder, mlb):
  try:
    df_car = pd.DataFrame([car_data])
    df_car = df_car.drop(['Condition'], axis=1, errors='ignore')

    # Aplicando Target Encoding para 'Car Model' (com o mesmo encoder usado no treino)
    df_car['Car Model_Encoded'] = te_encoder.transform(df_car['Car Model'])
    df_car = df_car.drop('Car Model', axis=1)

    # Aplicando o MultiLabelBinarizer para 'Options/Features'
    df_car['Options/Features_list'] = df_car['Options/Features'].apply(_split_features)
    X_features_encoded = mlb.transform(df_car['Options/Features_list'])
    
    # Coluna de nomes a partir do MLB para criar um DF
    feature_column_names = [f'Feature_{c}' for c in mlb.classes_]
    X_features_encoded_df = pd.DataFrame(X_features_encoded, columns=feature_column_names, index=df_car.index)

    # Juntar as features binarizadas com o DataFrame (removendo a coluna original 'Options/Features' e a lista temporária)
    cols_to_drop_after_mlb = ['Options/Features', 'Options/Features_list']
    df_car = pd.concat([df_car.drop(cols_to_drop_after_mlb, axis=1, errors='ignore'), X_features_encoded_df], axis=1)

    # --- Fim das Etapas de Pré-processamento Manual ---

    # Reordenar colunas para corresponder à ordem esperada pelo pipeline
    # O pipeline espera as colunas na ordem que foram apresentadas a ele DURANTE O TREINO.
    # A ordem no X_train_processed era:
    # 'Year', 'Mileage', 'Fuel Type', 'Color', 'Transmission', 'Accident', 'Car Model_Encoded'
    # MAIS as colunas Feature_... do MLB.
    # E o ColumnTransformer colocou OHE primeiro, depois remainder (numéricas + MLB).
    # A ordem final após o preprocessor do pipeline era:
    # Colunas OHE -> 'Car Model_Encoded', 'Year', 'Mileage' -> Colunas Feature_... MLB
    # Precisamos garantir que df_car tenha todas essas colunas e na ordem correta.

    # Identificar as colunas que devem existir após o pré-processamento manual
    
    categorical_ohe_cols = ['Fuel Type', 'Color', 'Transmission']
    numerical_cols_for_scaling = ['Year', 'Mileage', 'Car Model_Encoded', 'Accident_Encoded'] + feature_column_names
    expected_cols_before_pipeline = ['Car Model_Encoded', 'Year', 'Mileage', 'Fuel Type', 'Color', 'Transmission', 'Accident'] + feature_column_names

    # Garantir que todas as colunas esperadas existam em df_car, adicionando colunas com 0 se necessário
    # (para features MLB que não estavam na entrada, ou colunas categóricas OHE que não estavam)
    # E garantir a ordem correta
    df_car_aligned = pd.DataFrame(index=df_car.index)

    # Adicionar colunas na ordem esperada, preenchendo com 0 ou o valor existente
    for col in expected_cols_before_pipeline:
      if col in df_car.columns:
        df_car_aligned[col] = df_car[col]
      elif col.startswith('Feature_'): # Se for uma feature MLB esperada que não veio na entrada
        df_car_aligned[col] = 0 # Adiciona a coluna com 0

    # Certificar-se de que as colunas categóricas para OHE estão presentes, mesmo que vazias, antes de passá-las
    # para o preprocessor_pipeline (que espera essas colunas).
    # O OneHotEncoder handle_unknown='ignore' cuidará das categorias *dentro* dessas colunas.
    # Mas as colunas *elas mesmas* devem existir.
    for col in categorical_ohe_cols:
      if col not in df_car_aligned.columns:
        # Adiciona a coluna com um valor padrão (poderia ser NaN, ou um valor que o OHE ignore)
        # Usar None/NaN para que o OneHotEncoder com handle_unknown='ignore' funcione corretamente.
        df_car_aligned[col] = None


    # Reordenar colunas para o formato exato que o pipeline espera APÓS o pré-processamento manual
    # A ordem das colunas em X_train_processed é a ordem que o pipeline espera.
    # Vamos usar as colunas de X_train_processed para reordenar df_car_aligned.
    # Certifique-se de que X_train_processed existe (execute as células de treino antes).
    expected_order = [
      'Year',
      'Mileage',
      'Fuel Type',
      'Color',
      'Transmission',
      'Accident',
      'Car Model_Encoded',
      'Feature_Backup Camera',
      'Feature_Bluetooth',
      'Feature_GPS',
      'Feature_Heated Seats',
      'Feature_Leather Seats',
      'Feature_Navigation',
      'Feature_Remote Start',
      'Feature_Sunroof'
    ]
    # Garantir que df_car_aligned tenha todas as colunas esperadas e na ordem correta
    # Cria um novo DataFrame com as colunas na ordem esperada, preenchendo com 0 ou None se faltar
    df_car_final_pipeline_input = pd.DataFrame(index=df_car_aligned.index)
    for col in expected_order:
      if col in df_car_aligned.columns:
        df_car_final_pipeline_input[col] = df_car_aligned[col]
      else:
        # Adicionar colunas faltantes (isso não deveria acontecer se expected_cols_before_pipeline estiver correto)
        # Mas como fallback, preencher com 0 para numéricas e None para categóricas
        if col in numerical_cols_for_scaling:
            df_car_final_pipeline_input[col] = 0
        elif col in categorical_ohe_cols:
            df_car_final_pipeline_input[col] = None
        else: # Features MLB que podem faltar se o mlb_loaded não as aprendeu (improvável)
            df_car_final_pipeline_input[col] = 0

    # Fazer a previsão usando o pipeline carregado
    prediction = model.predict(df_car_final_pipeline_input)

    # O predict retorna um array numpy, pegar o primeiro (e único) elemento
    predicted_price = float(prediction[0])

    return {"status": "success", "predicted_price": predicted_price}

  except Exception as e:
    # Capturar quaisquer erros durante o processamento e previsão
    import traceback
    return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}
