"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from __future__ import annotations

import discord


class ConfirmationView(discord.ui.View):
    def __init__(self, *, timeout: float, author_id: int, delete_after: bool) -> None:
        super().__init__(timeout=timeout)
        self.value: bool | None = None
        self.delete_after: bool = delete_after
        self.author_id: int = author_id
        self.message: discord.Message | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user.id == self.author_id:
            return True
        else:
            await interaction.response.send_message("This confirmation dialog is not for you.", ephemeral=True)
            return False

    async def on_timeout(self) -> None:
        if self.delete_after and self.message:
            if not self.message.flags.ephemeral:
                await self.message.delete()
            else:
                await self.message.edit(view=None, content="This is safe to dismiss now.")

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.defer()
        if self.delete_after and self.message:
            if not self.message.flags.ephemeral:
                await interaction.delete_original_response()
            else:
                await interaction.edit_original_response(view=None, content="This is safe to dismiss now.")

        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.defer()
        if self.delete_after and self.message:
            if not self.message.flags.ephemeral:
                await interaction.delete_original_response()
            else:
                await interaction.edit_original_response(view=None, content="This is safe to dismiss now.")

        self.stop()
