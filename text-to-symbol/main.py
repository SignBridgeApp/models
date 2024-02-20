import mxnet as mx
from sockeye import inference, model
import sentencepiece as spm
import warnings
warnings.filterwarnings("ignore")


device = mx.cpu()
model_folder = "spoken2symbol"
spm_path = model_folder + "/spm.model"


sockeye_models, sockeye_source_vocabs, sockeye_target_vocabs = model.load_models(
    context=device, dtype=None, model_folders=[model_folder], inference_only=True
)
sp = spm.SentencePieceProcessor(model_file=spm_path)


language_code = "en"
country_code = "ase" # "us"
translation_type = "sent"
n_best = 3
beam_size = n_best


def translate(text):
  
    tag_str = f"<2{language_code}> <4{country_code}> <{translation_type}>"
    formatted = f"{tag_str} {text}"
    encoded = " ".join(sp.encode(formatted, out_type=str))
    print(encoded)
    print()

    translator = inference.Translator(
        context=device,
        ensemble_mode="linear",
        scorer=inference.CandidateScorer(),
        output_scores=True,
        batch_size=1,
        beam_size=beam_size,
        beam_search_stop="all",
        nbest_size=n_best,
        models=sockeye_models,
        source_vocabs=sockeye_source_vocabs,
        target_vocabs=sockeye_target_vocabs,
    )

    encoded = inference.make_input_from_plain_string(0, encoded)
    output = translator.translate([encoded])[0]
    print(output)
    print()
    
    translations = []
    symbols_candidates = output.nbest_translations
    factors_candidates = output.nbest_factor_translations
    for symbols, factors in zip(symbols_candidates, factors_candidates):
        symbols = symbols.split(" ")
        xs = factors[0].split(" ")
        ys = factors[1].split(" ")
        fsw = ""

        for i, (symbol, x, y) in enumerate(zip(symbols, xs, ys)):
            if symbol != "P":
                if i != 0:
                    if (
                        not symbol.startswith("S")
                        or symbol.startswith("S387")
                        or symbol.startswith("S388")
                        or symbol.startswith("S389")
                        or symbol.startswith("S38a")
                        or symbol.startswith("S38b")
                    ):
                        fsw += " "
                fsw += symbol
                fsw += x
                fsw += "x"
                fsw += y

        translations.append(fsw)

    return translations

if __name__ == "__main__":
    spoken = "hi"
    symbol = translate(spoken)
    print(symbol)
    
    from signwriting.visualizer.visualize import signwriting_to_image

    fsw = symbol[0]
    img = signwriting_to_image(fsw)
    img.save("sign.png")
