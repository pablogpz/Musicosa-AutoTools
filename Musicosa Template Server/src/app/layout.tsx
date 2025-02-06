import React, { PropsWithChildren } from 'react'

import { MetadataFields } from '@/db/metadata'
import metadataRepository from '@/db/repository/metadata'

import './globals.css'

export default async function RootLayout({ children }: PropsWithChildren) {
    const editionMetadata = await metadataRepository.getMetadataByField(MetadataFields.edition)

    return (
        <html lang="es">
        <head>
            <meta charSet="utf-8"/>
            <meta content="width=device-width, initial-scale=1.0"/>
            <title>{`TFA ${(editionMetadata?.value)}`}</title>
        </head>
        <body>
            {children}
        </body>
        </html>
    )
}
