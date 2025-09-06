import { PropsWithChildren } from 'react'

import metadataRepository from '@/db/repositories/metadata'

import './globals.css'

export default async function RootLayout({ children }: PropsWithChildren) {
    const editionMetadata = await metadataRepository.getMetadataByField('edition')

    return (
        <html lang="es">
        <head>
            <meta charSet="utf-8"/>
            <meta content="width=device-width, initial-scale=1.0"/>
            <title>{`Musicosa ${(editionMetadata?.value)}`}</title>
        </head>
        <body>
        {children}
        </body>
        </html>
    )
}
