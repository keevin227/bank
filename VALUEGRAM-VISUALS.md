# ValueGram presentation visuals

The final two slides of the Bank Muscat presentation reuse the visual rendering code from the user-provided `keevin227/ValueGram` repository, revision `95137387d29db6717c660f4d4ebcd2c870dec747`.

Source modules:

- `tickup-main/tickup-main/features/brain/engine/`: original WebGL constellation renderer, model, layout, runtime lifecycle, graph activation, configuration and rendering quality modules.
- `tickup-main/tickup-main/features/brain-voice/model/paintVoiceOrb.ts`: original multicoloured canvas voice orb painter.

The presentation adapter supplies synthetic English banking entities and connections, local domain selection and a scripted CEO task-approval sequence. It does not include private organisation snapshots, customer records, API credentials, ValueGram backends or live microphone/task access. Banking integration remains proposed Stage 2 work.

Editable source remains in the locally ignored `presentation/valuegram/` directory. Bundle with the local presentation's esbuild installation:

```sh
cd presentation
./node_modules/.bin/esbuild valuegram/productEntry.js --bundle --format=iife --target=es2020 --minify --outfile=valuegram-visuals.js
```

The encrypted presentation builder embeds this bundle. Product-rendered posters preserve the final two visuals in the PDF and provide a graph fallback where WebGL is unavailable. The original reference repository is unchanged.
